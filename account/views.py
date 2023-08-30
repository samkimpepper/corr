from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic 
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from . models import *
from .serializers import *

class AccountViewSet(viewsets.ModelViewSet):
    permission_classes = []

    queryset = Account.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = []
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            raise serializers.ValidationError("비밀번호 불일치")

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)
        response = Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_200_OK)
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)

        return response 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.META.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()

        return JsonResponse({'msg': 'Successful Logout'}, status=status.HTTP_200_OK)
