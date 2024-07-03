from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("products", views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top_reviews/', views.top_reviews),
]
