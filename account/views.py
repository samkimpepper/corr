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
    def post(self, request):
        serializer = TokenObtainPairSerializer.get_token(request.data)
        