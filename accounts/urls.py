from django.urls import path
from .views import RegistrationView,OtpVerificationView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
     path('verify-otp/', OtpVerificationView.as_view(), name='verify-otp'),
]

