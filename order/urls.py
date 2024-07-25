from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("delivery_address", views.DeliveryAddressViewSet,
                basename='deliveryaddress')

urlpatterns = [
    path('', include(router.urls)),
    path("orders/", views.OrderView.as_view())
]
