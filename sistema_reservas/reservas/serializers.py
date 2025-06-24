from rest_framework import serializers
from .models import Reserva
from usuarios.models import UsuarioCliente, DisponibilidadMedico
from django.utils.translation import gettext as _


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'paciente', 'medico', 'fecha_inicio', 'fecha_fin', 'motivo', 'estado']
        read_only_fields = ['estado']

    def validate(self, data):
        medico = data['medico']
        paciente = data['paciente']
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']

        if not medico.is_medico:
            raise serializers.ValidationError("El usuario seleccionado no es un médico.")
        if not paciente.is_cliente:
            raise serializers.ValidationError("El paciente debe ser un cliente válido.")
        if fecha_inicio >= fecha_fin:
            raise serializers.ValidationError("La fecha de inicio debe ser menor a la fecha de fin.")

        dia_semana = fecha_inicio.weekday()
        disponibilidad = DisponibilidadMedico.objects.filter(
            medico=medico,
            dia_semana=dia_semana,
            hora_inicio__lte=fecha_inicio.time(),
            hora_fin__gte=fecha_fin.time()
        ).first()
        if not disponibilidad:
            raise serializers.ValidationError("El médico no tiene disponibilidad en ese horario.")

        conflicto = Reserva.objects.filter(
            medico=medico,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio
        ).exists()
        if conflicto:
            raise serializers.ValidationError("El médico ya tiene una reserva en ese horario.")

        return data

    def create(self, validated_data):
        return Reserva.objects.create(**validated_data)
