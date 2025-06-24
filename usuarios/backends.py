# usuarios/backends.py
from django.contrib.auth.backends import ModelBackend
from .models import UsuarioCliente

class AutenticacionPorRutBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UsuarioCliente.objects.get(rut=username)
        except UsuarioCliente.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
