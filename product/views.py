from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
