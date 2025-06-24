from django.db import models

class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('confirmacion', 'Confirmación'),
        ('recordatorio', 'Recordatorio'),
        ('cancelacion', 'Cancelación'),
    ]

    destinatario = models.EmailField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    contenido = models.TextField()
    enviada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_tipo_display()} a {self.destinatario}"
