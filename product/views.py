from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
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

    @action(detail=True, methods=['POST'])
    def upload_product_image(self, request, pk=None):
        product = get_object_or_404(models.Product, pk=pk)

        images = request.FILES.getlist('images')
        serialized_data = []

        for image in images:
            data = {'product': product.id, 'images': image}
            serialized_data.append(data)

        serializer = serializers.ProductImageSerializer(
            data=serialized_data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"])
    def all_categories(self, request):
        categories = models.Category.objects.all()
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def all_sizes(self, request):
        categories = models.Size.objects.all()
        serializer = serializers.SizeSerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def all_colors(self, request):
        categories = models.Color.objects.all()
        serializer = serializers.ColorSerializer(categories, many=True)
        return Response(serializer.data)
