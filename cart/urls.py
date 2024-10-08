from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartView.as_view()),
    path('cart/<int:product_id>/', views.CartView.as_view()),
    path('cart/delete_all/', views.delete_all_cart_products)
]
