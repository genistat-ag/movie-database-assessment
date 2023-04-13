from django.urls import path, include
from authentication.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .serializers import JwtAuthenticationSerializer


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(serializer_class=JwtAuthenticationSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]
