from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, nombre_completo, email=None, password=None, **extra_fields):
        if not nombre_completo:
            raise ValueError("El nombre completo es obligatorio.")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(nombre_completo=nombre_completo, email=email, username=nombre_completo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_completo, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')

        return self.create_user(nombre_completo, email, password, **extra_fields)

class UsuarioCliente(AbstractUser):
    rut = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nombre_completo = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    is_cliente = models.BooleanField(default=True)
    is_medico = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    # 👇 Agrega related_name para evitar conflicto
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_cliente_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_cliente_set',
        blank=True
    )

    objects = UsuarioManager()

    USERNAME_FIELD = 'rut'
    REQUIRED_FIELDS = ['nombre_completo', 'email']

    def es_medico(self):
        return self.is_medico and not self.is_admin

    def es_cliente(self):
        return self.is_cliente and not self.is_admin

    def es_admin(self):
        return self.is_admin

    def __str__(self):
        return f"{self.nombre_completo} es: {'Médico' if self.is_medico else 'Cliente'}"
    
class DisponibilidadMedico(models.Model):
    medico = models.ForeignKey(
        'usuarios.UsuarioCliente',
        on_delete=models.CASCADE,
        limit_choices_to={'is_medico': True}
    )
    dia_semana = models.IntegerField(choices=[(i, ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][i]) for i in range(7)])
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.medico.nombre_completo} - {self.get_dia_semana_display()} de {self.hora_inicio} a {self.hora_fin}"

