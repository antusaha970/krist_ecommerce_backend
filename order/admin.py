from django.contrib import admin
from .models import DeliveryAddress, Order, OrderItem

admin.site.register(DeliveryAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
