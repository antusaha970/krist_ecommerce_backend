from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Color)
admin.site.register(models.Review)
admin.site.register(models.Size)
admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductReviews)
