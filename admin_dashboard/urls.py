from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("messages", views.ClientMessageViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('overview/', views.admin_overview),
    path('latest_product/', views.admin_latest_products),
]
