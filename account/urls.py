from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from . import views 

app_name = 'account'

router = DefaultRouter()
#router.register('register', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh/', TokenVerifyView.as_view()),
    path('verify/', TokenRefreshView.as_view()),

    path('google/login/', views.google_login),
    path('google/callback/', views.google_callback),
    path('google/login/finish/', views.GoogleLogin.as_view()),
]