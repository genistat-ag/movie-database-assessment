from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # here permission class not required
    # permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer
