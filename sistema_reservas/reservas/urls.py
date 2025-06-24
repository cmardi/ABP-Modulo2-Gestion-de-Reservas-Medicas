from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet, validar_disponibilidad, ApiRootView

router = DefaultRouter()
router.register(r'reservas', ReservaViewSet, basename='reserva')

urlpatterns = [
    path('', ApiRootView.as_view(), name='api-root'),  # GET /api/
    path('validar-disponibilidad/', validar_disponibilidad, name='validar-disponibilidad'),
    path('', include(router.urls)),                    # /api/reservas/
]