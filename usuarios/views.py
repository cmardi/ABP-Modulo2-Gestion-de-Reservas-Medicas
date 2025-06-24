from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import PerfilUsuarioSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PerfilUsuarioSerializer, CustomTokenObtainPairSerializer  # Asegúrate que existan
from rest_framework import status
#from .models import UsuarioCliente

class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        serializer = PerfilUsuarioSerializer(usuario)
        return Response(serializer.data)


class CustomObtainJWTView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from .serializers import PerfilUsuarioSerializer

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        serializer = PerfilUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)