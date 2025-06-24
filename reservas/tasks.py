import boto3
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def enviar_notificacion_reserva(email, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        'no-reply@clinicadigital.com',  # remitente
        [email],
        fail_silently=False,
    )

@shared_task
def enviar_sms_sns(numero_telefono, mensaje):
    client = boto3.client('sns')

    response = client.publish(
        PhoneNumber=numero_telefono,
        Message=mensaje
    )
    return response