from django.urls import path
from . import views


urlpatterns = [
    path('accounts/register/', views.AccountRegistrationView.as_view()),
    path('accounts/login/', views.AccountLoginView.as_view()),
    path('accounts/me/', views.AccountUpdateView.as_view()),
    path('accounts/forgot_password/', views.send_forgot_password),
]
