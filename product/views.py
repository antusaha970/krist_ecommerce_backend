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
from order.models import Order
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    pagination_class = ProductPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
        categories = cache.get("categories")
        if categories is None:
            categories = models.Category.objects.all()
            cache.set("categories", categories, timeout=60*5)
        serializer = serializers.CategorySerializer(categories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def all_sizes(self, request):
        sizes = cache.get("sizes")
        if sizes is None:
            sizes = models.Size.objects.all()
            cache.set("sizes", sizes, timeout=60*5)
        serializer = serializers.SizeSerializer(sizes, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def all_colors(self, request):
        colors = cache.get("colors")
        if colors is None:
            colors = models.Color.objects.all()
            cache.set("colors", colors, timeout=60*5)
        serializer = serializers.ColorSerializer(colors, many=True)
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
            account = request.user

            is_ordered = Order.objects.filter(
                account=account, items__product=pk).exists()

            if not is_ordered:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            review_data = {
                'name': data.get('name'),
                'email': data.get('email'),
                'body': data.get('body'),
                'reviewer': account.id
            }

            review_serializer = serializers.ReviewValidatorSerializer(
                data=review_data, many=False)
            if review_serializer.is_valid():
                review_data['reviewer'] = account
                review = models.Review.objects.create(**review_data)
                pd_review = {'product': product, 'reviews': review}

                product_review = models.ProductReviews.objects.create(
                    **pd_review)
                product_review.save()

                return Response(status=status.HTTP_201_CREATED)
            return Response(review_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def add_category(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'details': "New category added"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def top_reviews(request):
    reviews = cache.get("reviews")
    if reviews is None:
        reviews = models.Review.objects.all()[0:10]
        cache.set("reviews", reviews, timeout=60*5)

    serializer = serializers.ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
