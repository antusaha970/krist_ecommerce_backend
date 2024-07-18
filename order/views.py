from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account = self.request.user
        return DeliveryAddress.objects.filter(account=account)

    def perform_create(self, serializer):
        account = self.request.user
        serializer.save(account=account)
