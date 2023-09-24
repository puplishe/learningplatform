from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfle


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email'),
        )
        user.set_password(validated_data['password'])
        user.save()
        UserProfle.objects.create(user=user)
        return user
