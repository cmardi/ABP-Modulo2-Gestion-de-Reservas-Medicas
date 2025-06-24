import pytest
from datetime import datetime, timedelta, time
from django.utils.timezone import make_aware
from django.urls import reverse
from rest_framework_jwt.settings import api_settings
from reservas.models import Reserva
from usuarios.models import UsuarioCliente, DisponibilidadMedico
from reservas.serializers import ReservaSerializer
from usuarios.utils import jwt_encode_handler, jwt_payload_handler


@pytest.mark.django_db
def test_cancelar_reserva(api_client, crear_usuarios):
    paciente, medico = crear_usuarios()

    # Token JWT para autenticación del paciente
    token = jwt_encode_handler(jwt_payload_handler(paciente))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # Crear disponibilidad
    DisponibilidadMedico.objects.create(
        medico=medico,
        dia_semana=0,
        hora_inicio=time(9, 0),
        hora_fin=time(12, 0)
    )

    # Crear reserva activa
    inicio = make_aware(datetime(2025, 6, 16, 9, 0))
    fin = inicio + timedelta(minutes=30)
    reserva = Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=inicio,
        fecha_fin=fin,
        motivo="Reserva a cancelar",
        estado="activa"
    )

    url = reverse('reserva-detail', args=[reserva.id])
    response = api_client.patch(url, {"estado": "cancelada"}, format='json')

    assert response.status_code == 200
    assert response.data["estado"] == "cancelada"

@pytest.mark.django_db
def test_listar_reservas_de_usuario(api_client, crear_usuarios):
    paciente, medico = crear_usuarios()
    token = jwt_encode_handler(jwt_payload_handler(paciente))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # Crear disponibilidad y reservas
    DisponibilidadMedico.objects.create(
        medico=medico,
        dia_semana=0,
        hora_inicio=time(9, 0),
        hora_fin=time(12, 0)
    )

    inicio = make_aware(datetime(2025, 6, 16, 10, 0))
    Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=inicio,
        fecha_fin=inicio + timedelta(minutes=30),
        motivo="Consulta 1"
    )
    Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=inicio + timedelta(hours=1),
        fecha_fin=inicio + timedelta(hours=1, minutes=30),
        motivo="Consulta 2"
    )

    url = reverse('reserva-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert all(res['paciente'] == paciente.id for res in response.data)

@pytest.mark.django_db
def test_cancelar_reserva_con_accion_personalizada(api_client, crear_usuarios):
    paciente, medico = crear_usuarios()
    token = jwt_encode_handler(jwt_payload_handler(paciente))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # Disponibilidad
    DisponibilidadMedico.objects.create(
        medico=medico,
        dia_semana=0,
        hora_inicio=time(9, 0),
        hora_fin=time(12, 0)
    )

    # Crear reserva
    inicio = make_aware(datetime(2025, 6, 16, 9, 0))
    reserva = Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=inicio,
        fecha_fin=inicio + timedelta(minutes=30),
        motivo="Reserva cancelable",
        estado="activa"
    )

    url = reverse('reserva-cancelar', args=[reserva.id])  # usar nombre basado en la acción
    response = api_client.post(url)

    assert response.status_code == 200
    assert response.data["estado"] == "cancelada"

@pytest.mark.django_db
def test_cliente_no_puede_completar(api_client, crear_usuarios):
    paciente, medico = crear_usuarios()
    token = jwt_encode_handler(jwt_payload_handler(paciente))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    reserva = Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=make_aware(datetime(2025, 6, 16, 10, 0)),
        fecha_fin=make_aware(datetime(2025, 6, 16, 10, 30)),
        motivo="Intento inválido",
        estado="activa"
    )

    url = reverse('reserva-completar', args=[reserva.id])
    response = api_client.post(url)

    assert response.status_code == 403
    assert "permiso" in str(response.data).lower()


@pytest.mark.django_db
def test_medico_no_puede_cancelar(api_client, crear_usuarios):
    paciente, medico = crear_usuarios()
    token = jwt_encode_handler(jwt_payload_handler(medico))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    reserva = Reserva.objects.create(
        paciente=paciente,
        medico=medico,
        fecha_inicio=make_aware(datetime(2025, 6, 16, 10, 0)),
        fecha_fin=make_aware(datetime(2025, 6, 16, 10, 30)),
        motivo="Intento inválido",
        estado="activa"
    )

    url = reverse('reserva-cancelar', args=[reserva.id])
    response = api_client.post(url)

    assert response.status_code == 403
    assert "permiso" in str(response.data).lower()
