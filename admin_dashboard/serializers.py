from rest_framework import serializers
from .models import ClientMessage


class ClientMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientMessage
        fields = "__all__"
