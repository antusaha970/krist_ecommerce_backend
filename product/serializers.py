from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name', 'thumbnail']


class ReviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ReviewerSerializer()

    class Meta:
        model = models.Review
        fields = "__all__"


class ReviewValidatorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Review
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = ['name']


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = ['name']


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=False)

    class Meta:
        model = models.ProductReviews
        fields = ['reviews']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ['images']


class ProductImageToDisplay(serializers.Serializer):
    # images = serializers.SerializerMethodField()

    # def get_images(self, obj):
    #     request = self.context.get('request')
    #     if request is not None:
    #         return request.build_absolute_uri(obj.images.url)
    #     return obj.images.url  # fallback if request context is missing

    class Meta:
        model = models.ProductImage
        fields = ['images']


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)

    categories = serializers.SlugRelatedField(
        queryset=models.Category.objects.all(), slug_field='name', many=True)
    colors = serializers.SlugRelatedField(
        queryset=models.Color.objects.all(), slug_field='name', many=True)
    sizes = serializers.SlugRelatedField(
        queryset=models.Size.objects.all(), slug_field='name', many=True)

    class Meta:
        model = models.Product
        fields = "__all__"
        extra_kwargs = {
            'price': {'required': True},
            'title': {'required': True},
            'description': {'required': True},
            'stock': {'required': True},
            'additional_info': {'required': True},
            'categories': {'required': True},
            'colors': {'required': True},
            'sizes': {'required': True},
        }

    def create(self, validated_data):
        categories_data = validated_data.pop('categories')
        colors_data = validated_data.pop('colors')
        sizes_data = validated_data.pop('sizes')

        product = models.Product.objects.create(**validated_data)

        product.categories.set(categories_data)
        product.colors.set(colors_data)
        product.sizes.set(sizes_data)

        product.save()
        return product
