import pytest
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware

from usuarios.models import UsuarioCliente, DisponibilidadMedico
from reservas.models import Reserva
from reservas.serializers import ReservaSerializer

@pytest.mark.django_db
def test_crea_reserva_valida():
    paciente = UsuarioCliente.objects.create_user(
        nombre_completo="Paciente Uno", email="p1@correo.com", password="123", rut="11", is_cliente=True
    )
    medico = UsuarioCliente.objects.create_user(
        nombre_completo="Doctor Uno", email="m1@correo.com", password="123", rut="22", is_medico=True
    )

    # Lunes
    DisponibilidadMedico.objects.create(
        medico=medico,
        dia_semana=0,
        hora_inicio=time(9, 0),
        hora_fin=time(12, 0)
    )

    inicio = make_aware(datetime(2025, 6, 16, 9, 30))  # Lunes
    fin = inicio + timedelta(minutes=30)

    data = {
        "paciente": paciente.id,
        "medico": medico.id,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "motivo": "Chequeo"
    }

    serializer = ReservaSerializer(data=data)
    assert serializer.is_valid(), serializer.errors

    reserva = serializer.save()
    assert reserva.paciente == paciente
    assert reserva.medico == medico


@pytest.mark.django_db
def test_falla_si_sin_disponibilidad():
    paciente = UsuarioCliente.objects.create_user(
        nombre_completo="Paciente Dos", email="p2@correo.com", password="123", rut="33", is_cliente=True
    )
    medico = UsuarioCliente.objects.create_user(
        nombre_completo="Doctor Dos", email="m2@correo.com", password="123", rut="44", is_medico=True
    )

    inicio = make_aware(datetime(2025, 6, 17, 10, 0))  # Martes sin disponibilidad
    fin = inicio + timedelta(minutes=30)

    data = {
        "paciente": paciente.id,
        "medico": medico.id,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "motivo": "Sin disponibilidad"
    }

    serializer = ReservaSerializer(data=data)
    assert not serializer.is_valid()
    assert "El médico no tiene disponibilidad" in str(serializer.errors)


@pytest.mark.django_db
def test_falla_por_conflicto_de_reserva():
    paciente1 = UsuarioCliente.objects.create_user(
        nombre_completo="Paciente Uno", email="p1@correo.com", password="123", rut="55", is_cliente=True
    )
    paciente2 = UsuarioCliente.objects.create_user(
        nombre_completo="Paciente Dos", email="p2@correo.com", password="123", rut="66", is_cliente=True
    )
    medico = UsuarioCliente.objects.create_user(
        nombre_completo="Doctor Tres", email="m3@correo.com", password="123", rut="77", is_medico=True
    )

    DisponibilidadMedico.objects.create(
        medico=medico,
        dia_semana=2,
        hora_inicio=time(10, 0),
        hora_fin=time(12, 0)
    )

    inicio = make_aware(datetime(2025, 6, 18, 10, 30))  # Miércoles
    fin = inicio + timedelta(minutes=30)

    # Reserva inicial
    Reserva.objects.create(
        paciente=paciente1,
        medico=medico,
        fecha_inicio=inicio,
        fecha_fin=fin,
        motivo="Ya existe"
    )

    # Segunda reserva en conflicto
    data = {
        "paciente": paciente2.id,
        "medico": medico.id,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "motivo": "Conflicto"
    }

    serializer = ReservaSerializer(data=data)
    assert not serializer.is_valid()
    assert "El médico ya tiene una reserva" in str(serializer.errors)
