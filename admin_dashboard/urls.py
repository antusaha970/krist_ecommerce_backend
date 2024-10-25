from django.urls import path
from . import views


urlpatterns = [
    path('overview/', views.admin_overview),
    path('latest_product/', views.admin_latest_products),
]
