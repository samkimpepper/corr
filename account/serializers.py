from rest_framework import serializers
from datetime import datetime, time
from enum import Enum
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'username']

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account