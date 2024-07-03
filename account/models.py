from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class Account(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=12, default=None, null=True)
    profile_picture = models.ImageField(
        upload_to="account/profile", default="profile.jgp")
    address = models.CharField(max_length=300, default="", blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
