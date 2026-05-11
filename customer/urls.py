from django.urls import path
from .views import (
    CustomerRegisterView,
    CustomerLoginView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [

    path( 'register/', CustomerRegisterView.as_view(), name='register'),
    path( 'login/', CustomerLoginView.as_view(), name='login'),
    path( 'forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path( 'reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]