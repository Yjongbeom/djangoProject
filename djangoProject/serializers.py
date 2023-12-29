from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'division',
        )

class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'division',
            'password',
        )
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            division=validated_data['division'],
            password=validated_data['password']
        )
        return user