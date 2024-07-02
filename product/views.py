from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from .filters import ProductFilter
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        filterset = ProductFilter(
            self.request.GET, queryset=models.Product.objects.all().order_by('id'))
        return filterset.qs
