from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class ProductPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        filterset = ProductFilter(
            self.request.GET, queryset=models.Product.objects.all().order_by('id'))
        return filterset.qs
