from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    reviewer = models.ForeignKey(
        get_user_model(), null=True, blank=True, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    body = models.TextField()

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    categories = models.ManyToManyField(
        Category, related_name="productCategory",  default=None)
    colors = models.ManyToManyField(
        Color, related_name="productColor", default="", blank=True)

    price = models.DecimalField(max_digits=7, decimal_places=2)
    sizes = models.ManyToManyField(
        Size, related_name="productSize", default="", blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=300, unique=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    additional_info = models.TextField()
    slug = models.SlugField(default=None, null=True, blank=True)
    owner = models.ForeignKey(
        get_user_model(), null=True, blank=True, default=None, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images")
    images = models.ImageField(upload_to="product/images")


class ProductReviews(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_reviews")
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE)
