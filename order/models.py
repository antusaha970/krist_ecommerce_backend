from django.db import models
from django.contrib.auth import get_user_model


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
