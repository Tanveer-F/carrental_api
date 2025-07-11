from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import VehicleViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet, basename='vehicles')

urlpatterns = [
    path('', include(router.urls)),
]
