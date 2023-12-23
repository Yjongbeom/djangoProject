from rest_framework import serializers
from . import models
from .models import User


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'password',
        )
        model = models.User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'