from django.shortcuts import render, redirect
from django.conf import settings 
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic 
from django.views.generic import View, TemplateView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import requests 
from json.decoder import JSONDecodeError

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google import views as google_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Create your views here.
from . models import *
from .serializers import *
   
class RegisterView(APIView):
    permission_classes = []
    def post(self, request):
        data = request.data 
        serializer = RegisterSerializer(data=data)
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

STATE = getattr(settings, 'STATE')
BASE_URL = 'http://localhost:8000/'
GOOGLE_CALLBACK_URI = BASE_URL + 'account/google/callback/'
CLIENT_ID = getattr(settings, "SOCIAL_AUTH_GOOGLE_CLIENT_ID")
CLIENT_SECRET = getattr(settings, "SOCIAL_AUTH_GOOGLE_SECRET")

def google_login(request):
    # Code request
    scope = "https://www.googleapis.com/auth/userinfo.email"

    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    code = request.GET.get('code')
    access_token = get_access_token(code)
    email = get_user_info(access_token)

    # Signup or Signin Request
    try:
        user = Account.objects.get(email=email)
        social_user = SocialAccount.objects.get(user=user)
        if social_user is None:
            return JsonResponse({'msg': 'email exists but not social user'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(f"{BASE_URL}account/google/login/finish/", data=data)
        accept_status = accept.status_code 
        if accept_status != 200:
            return JsonResponse({'msg': 'failed to signin'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    except Account.DoesNotExist:
        data = {'access_token': access_token, 'code': code}
        accept = requests.post(
            f"{BASE_URL}account/google/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({'msg': 'failed to signup'}, status=accept_status)
        accept_json = accept.json()
        accept_json.pop('user', None)
        return JsonResponse(accept_json)
    
class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter 
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client

def get_access_token(code):
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={STATE}")
    token_req_json = token_req.json()
    err = token_req_json.get("error")
    if err is not None:
        raise JSONDecodeError(err)
    
    access_token = token_req_json.get('access_token')
    return access_token

def get_user_info(access_token):
    email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
    email_req_status = email_req.status_code
    if email_req_status != 200:
        return JsonResponse({'msg': 'failed to get email'}, status=status.HTTP_400_BAD_REQUEST)
    
    email_req_json = email_req.json()
    email = email_req_json.get('email')
    return email 