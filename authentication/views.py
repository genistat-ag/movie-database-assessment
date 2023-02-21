from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from rest_framework import generics


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # any user can register
    serializer_class = RegisterSerializer
