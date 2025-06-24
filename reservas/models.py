from django.db import models
from usuarios.models import UsuarioCliente  
from recursos.models import Sala

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cancelada', 'Cancelada'),
        ('completada', 'Completada'),
    ]

    paciente = models.ForeignKey(
        UsuarioCliente,
        on_delete=models.CASCADE,
        related_name='reservas_paciente',
        limit_choices_to={'is_cliente': True}
    )

    medico = models.ForeignKey(
        UsuarioCliente,
        on_delete=models.CASCADE,
        related_name='reservas_medico',
        limit_choices_to={'is_medico': True}
    )

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    motivo = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')

    creada_en = models.DateTimeField(auto_now_add=True)
    
    sala = models.ForeignKey(Sala, on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_duracion(self):
        return (self.fecha_fin - self.fecha_inicio).total_seconds() / 60  

    def __str__(self):
        return f"Reserva de {self.paciente.nombre_completo} con {self.medico.nombre_completo} el {self.fecha_inicio}"
