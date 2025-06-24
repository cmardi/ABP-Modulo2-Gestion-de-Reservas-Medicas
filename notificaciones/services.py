from django.core.mail import send_mail
from django.conf import settings

class NotificacionService:
    @staticmethod
    def enviar_confirmacion(email, nombre, fecha, medico):
        asunto = "Confirmación de reserva médica"
        mensaje = f"Hola {nombre}, tu reserva con el Dr. {medico} ha sido confirmada para el {fecha}."
        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [email])

    @staticmethod
    def enviar_recordatorio(email, nombre, fecha):
        asunto = "Recordatorio de reserva médica"
        mensaje = f"Hola {nombre}, te recordamos tu cita médica programada para el {fecha}."
        send_mail(asunto, mensaje, settings.DEFAULT_FROM_EMAIL, [email])
