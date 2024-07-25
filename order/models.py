from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from django.core.validators import MinValueValidator


class DeliveryAddress(models.Model):
    account = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="delivery_address")
    mobile_number = models.CharField(max_length=12)
    apartment = models.CharField(max_length=300)
    area = models.CharField(max_length=400)
    city = models.CharField(max_length=150)
    pin_code = models.IntegerField()
    state = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.account.email


ORDER_STATUS = [("processing", "processing"),
                ("delivered", "delivered"), ("shipped", "shipped")]
PAYMENT_STATUS = [("unpaid", "unpaid"), ("paid", "paid")]
PAYMENT_MODE = [("COD", "COD"), ("CARD", "CARD")]


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])


class Order(models.Model):
    address = models.ForeignKey(
        DeliveryAddress, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(
        max_length=25, choices=ORDER_STATUS, default="processing")
    payment_status = models.CharField(
        max_length=20, default="unpaid", choices=PAYMENT_STATUS)
    payment_mode = models.CharField(max_length=20, default="COD")
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem)
