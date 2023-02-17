from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import exceptions, serializers
from .serializers import RegisterSerializer,CustomeTokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer


class CustomeTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = CustomeTokenObtainPairSerializer


token_obtain_pair = CustomeTokenObtainPairView.as_view()