from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

def jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': {
            'rut': user.rut,
            'nombre_completo': user.nombre_completo,
            'email': user.email,
            'is_cliente': user.is_cliente,
            'is_medico': user.is_medico,
        }
    }
