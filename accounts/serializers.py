from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model()

class UserCreateSerializer(UserCreateSerializer):
    password_retype = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.TYPE, default=User.TYPE[0][0])

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'full_name', 'user_type','password','password_retype')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        password = attrs.get('password')
        password_retype = attrs.get('password_retype')

        if password != password_retype:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs







