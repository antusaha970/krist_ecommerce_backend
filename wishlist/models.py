from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
# Create your models here.


class WishList(models.Model):
    account = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="wishlist")
    products = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self) -> str:
        return self.account.email
