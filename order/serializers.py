from rest_framework import serializers
from .models import DeliveryAddress, Order, OrderItem
from product.serializers import ProductSerializer


class DeliveryAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = "__all__"
        extra_kwargs = {
            'account': {'required': False}
        }


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderDisplaySerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
