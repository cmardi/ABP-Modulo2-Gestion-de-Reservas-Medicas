from .models import Reserva
from notificaciones.services import NotificacionService
from datetime import datetime

def verificar_disponibilidad(medico, sala, fecha_inicio, fecha_fin):
    conflictos = Reserva.objects.filter(
        medico=medico,
        sala=sala,
        estado='activa',
        fecha_inicio__lt=fecha_fin,
        fecha_fin__gt=fecha_inicio
    )
    return not conflictos.exists()

def crear_reserva(paciente, medico, sala, fecha_inicio, fecha_fin, motivo=None):
    if fecha_inicio >= fecha_fin:
        raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")

    if not verificar_disponibilidad(medico, sala, fecha_inicio, fecha_fin):
        raise Exception("El médico o la sala no están disponibles en ese horario.")

    reserva = Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        sala=sala,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        motivo=motivo,
        estado='activa'
    )

    # Enviar notificación de confirmación
    NotificacionService.enviar_confirmacion(
        email=paciente.email,
        nombre=paciente.nombre_completo,
        fecha=fecha_inicio,
        medico=medico.nombre_completo
    )

    return reserva
