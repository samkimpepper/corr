from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView

from . import views 

router = DefaultRouter()
router.register('register', views.AccountViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenVerifyView.as_view()),
    path('verify/', TokenRefreshView.as_view()),
]