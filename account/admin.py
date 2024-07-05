from django.contrib import admin
from .models import Account, AccountPasswordResetProfile

admin.site.register(Account)
admin.site.register(AccountPasswordResetProfile)
