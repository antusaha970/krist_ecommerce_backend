from rest_framework import serializers
from .models import WishList
from product.serializers import ProductSerializer


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = "__all__"


class WishListForDisplaySerializer(serializers.ModelSerializer):
    products = ProductSerializer(read_only=True)

    class Meta:
        model = WishList
        fields = "__all__"
