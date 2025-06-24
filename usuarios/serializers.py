# from rest_framework import serializers
from .models import UsuarioCliente
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioCliente
        fields = ['id', 'nombre_completo', 'email', 'rut', 'telefono', 'direccion', 'fecha_nacimiento', 'is_cliente', 'is_medico', 'is_admin', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UsuarioCliente(**validated_data)
        user.set_password(password)
        user.save()
        return user



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Puedes agregar datos personalizados al token aquí
        data['username'] = self.user.username
        # data['email'] = self.user.email  # Descomenta si quieres incluir el email
        return data
    
