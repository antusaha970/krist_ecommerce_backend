from django.urls import path
from . import views


urlpatterns = [
    path('wishlist/', views.WishListView.as_view()),
    path('wishlist/<int:pk>/', views.WishListView.as_view()),
]
