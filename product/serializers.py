from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['name']


class ReviewSerializer(serializers.ModelSerializer):
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
        fields = "__all__"


class ProductImageToDisplay(serializers.Serializer):
    images = serializers.ImageField()


class ProductSerializer(serializers.ModelSerializer):
    product_images = ProductImageToDisplay(many=True, read_only=True)

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
