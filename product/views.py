from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from .filters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

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

    @action(detail=True, methods=["GET", "POST"])
    def product_review(self, request, pk=None):
        if request.method == "GET":
            reviews = get_list_or_404(models.ProductReviews, product__id=pk)
            serializer = serializers.ProductReviewsSerializer(
                reviews, many=True)
            return Response(serializer.data)

        if request.method == "POST":
            product = get_object_or_404(models.Product, pk=pk)
            data = request.data
            user = request.user
            review_data = {
                'name': data.get('name'),
                'email': data.get('email'),
                'body': data.get('body'),
                'reviewer': user.id
            }

            review_serializer = serializers.ReviewSerializer(
                data=review_data, many=False)
            if review_serializer.is_valid():
                review = models.Review.objects.create(**data)
                pd_review = {'product': product, 'reviews': review}
                product_review = models.ProductReviews.objects.create(
                    **pd_review)
                product_review.save()

                return Response(review_serializer.data)
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def top_reviews(request):
    reviews = models.Review.objects.all()[0:10]
    serializer = serializers.ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
