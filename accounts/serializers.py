from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
            'is_staff',
        ]


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=10)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=100)


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=10)
    password = serializers.CharField(required=True, max_length=100)