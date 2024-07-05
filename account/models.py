from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.dispatch import receiver
from django.db.models.signals import post_save


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


class AccountPasswordResetProfile(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name="ResetPassword")
    reset_password_otp = models.IntegerField(
        null=True, blank=True, default=None)
    reset_password_expire = models.DateTimeField(
        null=True, blank=True, default=None)


@receiver(post_save, sender=Account)
def make_profile_for_password_reset(sender, instance, created, **kwargs):
    """This signal automatically create a new profile after a account do registration"""
    account = instance
    if created:
        profile = AccountPasswordResetProfile(account=account)
        profile.save()
