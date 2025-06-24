from django.db import models
from usuarios.models import UsuarioCliente 

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
