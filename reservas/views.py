from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import datetime
from usuarios.models import DisponibilidadMedico
from .models import Reserva
from .serializers import ReservaSerializer
from .tasks import enviar_notificacion_reserva, enviar_sms_sns
from reservas.utils.notificaciones import (
    plantilla_sms_cancelacion,
    plantilla_sms_completada,
)

class ApiRootView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Bienvenido a la API",
            "endpoints": {
                "reservas": "/api/reservas/",
                "auth": "/api/auth/",
            }
        })

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_medico:
            return Reserva.objects.filter(medico=user)
        elif user.is_cliente:
            return Reserva.objects.filter(paciente=user)
        return Reserva.objects.none()

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if request.user != reserva.paciente:
            return Response({'error': 'No tiene permiso para cancelar esta reserva.'}, status=403)
        if reserva.estado == 'cancelada':
            return Response({'error': 'La reserva ya está cancelada.'}, status=400)
        if reserva.estado == 'completa':
            return Response({'error': 'No se puede cancelar una reserva completada.'}, status=400)
        reserva.estado = 'cancelada'
        reserva.save()
        enviar_notificacion_reserva.delay(
            reserva.medico.email,
            "Reserva cancelada",
            f"La reserva con el paciente {reserva.paciente.nombre_completo} ha sido cancelada."
        )
        if reserva.medico.telefono.startswith('+'):
            enviar_sms_sns.delay(reserva.medico.telefono, plantilla_sms_cancelacion('medico', reserva))
        if reserva.paciente.telefono.startswith('+'):
            enviar_sms_sns.delay(reserva.paciente.telefono, plantilla_sms_cancelacion('paciente', reserva))
        return Response({'mensaje': 'Reserva cancelada.', 'estado': reserva.estado}, status=200)

    @action(detail=True, methods=['post'], url_path='completar')
    def completar(self, request, pk=None):
        reserva = self.get_object()
        if request.user != reserva.medico:
            return Response({'error': 'No tiene permiso para completar esta reserva.'}, status=403)
        if reserva.estado == 'cancelada':
            return Response({'error': 'No se puede completar una reserva cancelada.'}, status=400)
        if reserva.estado == 'completa':
            return Response({'error': 'La reserva ya está completada.'}, status=400)
        reserva.estado = 'completa'
        reserva.save()
        enviar_notificacion_reserva.delay(
            reserva.paciente.email,
            "Consulta completada",
            f"Tu consulta con el Dr. {reserva.medico.nombre_completo} ha sido marcada como completada."
        )
        if reserva.paciente.telefono.startswith('+'):
            enviar_sms_sns.delay(reserva.paciente.telefono, plantilla_sms_completada('paciente', reserva))
        if reserva.medico.telefono.startswith('+'):
            enviar_sms_sns.delay(reserva.medico.telefono, plantilla_sms_completada('medico', reserva))
        return Response({'mensaje': 'Reserva completada.', 'estado': reserva.estado}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validar_disponibilidad(request):
    medico_id = request.data.get('medico')
    fecha_inicio = request.data.get('fecha_inicio')
    fecha_fin = request.data.get('fecha_fin')
    if not medico_id or not fecha_inicio or not fecha_fin:
        return Response({'disponible': False, 'error': 'Datos incompletos'}, status=400)
    try:
        inicio = datetime.fromisoformat(fecha_inicio)
        fin = datetime.fromisoformat(fecha_fin)
    except ValueError:
        return Response({'disponible': False, 'error': 'Formato de fecha inválido.'}, status=400)
    dia = inicio.weekday()
    esta_disponible = DisponibilidadMedico.objects.filter(
        medico_id=medico_id,
        dia_semana=dia,
        hora_inicio__lte=inicio.time(),
        hora_fin__gte=fin.time()
    ).exists()
    if not esta_disponible:
        return Response({'disponible': False, 'error': 'El médico no está disponible en ese horario.'}, status=200)
    conflictos = Reserva.objects.filter(
        medico_id=medico_id,
        fecha_inicio__lt=fin,
        fecha_fin__gt=inicio,
        estado='activa'
    ).exists()
    if conflictos:
        return Response({'disponible': False, 'error': 'El médico ya tiene una reserva en ese horario.'}, status=200)
    return Response({'disponible': True}, status=200)