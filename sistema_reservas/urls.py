from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenRefreshView
from usuarios.token_views import CustomTokenObtainPairView, RegistroUsuarioView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('reservas.urls')),         # Rutas de la app reservas
    path('api/auth/', include('usuarios.urls')),    # Rutas de la app usuarios
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
    path('api/auth/register/', RegistroUsuarioView.as_view(), name='registro-usuario'),
]