from datetime import datetime
from aiohttp import request
from django.utils import timezone 
from rest_framework import generics
from rest_framework.response import Response
from .serializers import RegistrationSerializer, OtpVerificationSerializer,ProfileSerializer
from .utils import  generate_otp,send_sms
from .models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response

class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        full_name = request.data.get('full_name')

        existing_user = User.objects.filter(phone_number=phone_number).first()

        if existing_user:
            if not existing_user.is_active:
                existing_user.delete()
            else:
                return Response(
                    {'phone_number': ['User with this phone number already exists.']},
                    status=status.HTTP_400_BAD_REQUEST
                )

        otp = generate_otp()
        user = User.objects.create_user(
            phone_number=phone_number,
            full_name=full_name,
            verification_code=otp,
            otp_generation_time =  timezone.now()
        )
        send_sms(otp, phone_number)

        response_data = {'message': 'User registered successfully.'}

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class OtpVerificationView(generics.CreateAPIView):
    serializer_class = OtpVerificationSerializer

    def create(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')
        user = User.objects.get(phone_number = phone_number)
        if not user:
            response_data = {'message': 'User does not exist'}
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        else:
            if user.verification_code == verification_code:
                if user.valid_otp():
                    token, created = Token.objects.get_or_create(user=user)
                    response_data = {
                        'message': 'Successfully logged in',
                        'token': token.key 
                        }
                    user.is_active = True
                    user.save()
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {'message': 'This verification code has expired'}
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {'message': 'Incorrect verification code'}
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            

# class ProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = ProfileSerializer
#     permission_classes = [IsAuthenticated]
#     def get_queryset(self):
#         return User.objects.filter(id=self.request.user.id)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    


        

