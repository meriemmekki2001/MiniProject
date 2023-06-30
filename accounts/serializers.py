from rest_framework import serializers
from .models import User



class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_number','full_name']
        read_only_fields = ['id']
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        if not phone_number:
            raise serializers.ValidationError("Phone number is required.")
        return data
    


class OtpVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','phone_number','verification_code']
        read_only_fields = ['id']
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        verification_code = data.get('verification_code')
        if not phone_number:
            raise serializers.ValidationError("Please Enter your phone number.")
        if not verification_code:
            raise serializers.ValidationError("Please Enter your verification code")
        return data
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name','email','phone_number','adress']




    

    

        

    