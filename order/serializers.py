from rest_framework import serializers
from .models import DeliveryAddress


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = "__all__"
        extra_kwargs = {
            'account': {'required': False}
        }
