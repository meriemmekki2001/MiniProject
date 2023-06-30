from django.urls import path
from .views import RegistrationView,OtpVerificationView,ProfileView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='registration'),
     path('verify-otp/', OtpVerificationView.as_view(), name='verify-otp'),
     path('profile/me/', ProfileView.as_view(), name='profile'),
    
]

