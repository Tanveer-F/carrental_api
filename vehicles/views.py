from rest_framework import viewsets
from .models import Vehicle
from .serializers import VehicleSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        # Return only vehicles owned by the logged-in user
        return Vehicle.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner as the logged-in user
        serializer.save(owner=self.request.user)
