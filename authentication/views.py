from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAdminUser


class RegisterView(generics.CreateAPIView):
    """
    User Registerion. Only Admin user's can register user to the site.

    Registration Requirements:
    - Username: system's unique username
    - Email : System's unique email id
    - Password: minimum 8 characert long, cannot be too common, cannot be entirely numeric.
    - Password2: Must be similar to the Password field.
    """
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer
    