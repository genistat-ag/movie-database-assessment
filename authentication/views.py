from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)   #bug 5
    serializer_class = RegisterSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer