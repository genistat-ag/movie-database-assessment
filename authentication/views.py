from tokenize import TokenError

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser, AllowAny
from django.contrib.auth import login
from .email_phone_auth import EmailUsernameAuthenticationBackend as EUA


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    """
    JWT Custom Token Claims View
    custom authentication view created to login with username or email and password
    also custom serializer is used to return custom claims
    """

    serializer_class = CustomTokenObtainPairSerializer

    @staticmethod
    def _direct_login(request, user, serializer):
        """
        Method for login
        """
        login(request, user)  # authenticate user
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = EUA.authenticate(
                request=request,
                username=request.data.get("username"),
                password=request.data.get("password"),
            )  # get user from authenticate method using username or email and password
            try:
                return self._direct_login(
                    request=request, user=user, serializer=serializer
                )

            except TokenError as e:
                raise InvalidToken(e.args[0]) from e

        except Exception:
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
