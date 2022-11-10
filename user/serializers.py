from django.contrib.auth.models import User
from rest_framework import serializers
from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']
