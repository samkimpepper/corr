from rest_framework import serializers
from datetime import datetime, time
from enum import Enum
from .models import *
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'password', 'username']

    def validate(self, data):
        email = data.get('email')
        is_exists = Account.objects.filter(email=email).exists()
        if is_exists:
            raise serializers.ValidationError("존재하는 이메일")
        return data 

    def create(self, validated_data):
        account = Account.objects.create_user(**validated_data)
        return account
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    check_password = serializers.CharField(write_only=True)

    def validate(self, data):
        password = data.get('password')
        check_password = data.get('check_password')

        if password != check_password:
            raise serializers.ValidationError("비밀번호 확인 불일치")

        return data