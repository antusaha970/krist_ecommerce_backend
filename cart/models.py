from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product


class Cart(models.Model):
    account = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.account.email
