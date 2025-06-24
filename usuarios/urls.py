from django.urls import path
from .views import PerfilUsuarioView
from .token_views import *
#from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomObtainJWTView

urlpatterns = [
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomObtainJWTView.as_view(), name='token_obtain_pair'),
    path('register/', RegistroUsuarioView.as_view(), name='registro-usuario'),
]
