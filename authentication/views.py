from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import RegisterSerializer, UserLogInTokenObtainPairSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    """Create this view for meet
    Users should be able to log in with both the below combinations
        ○ username and password
        ○ email and password
    """

    def post(self, request, *args, **kwargs) -> dict:
        data = request.data.copy()
        username_or_email = data.get("username_or_email")
        if not username_or_email:
            return Response({"error": "username_or_email not specified."}, status=400)
        user = self.get_user(username_or_email=username_or_email)
        if not user:
            return Response({"error": "User Not Found."}, status=404)
        data['username'] = user.username
        serializer = UserLogInTokenObtainPairSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_user(self, username_or_email: str) -> dict:
        return User.objects.filter(
            Q(email=username_or_email) | Q(username=username_or_email)
        ).first()