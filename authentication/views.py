from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    A view that handles user registration.

    Allows an administrator user to register new users by sending a POST request with a JSON payload to the URL endpoint associated with this view. The payload must contain the following fields:

    - username: the username of the new user (string, required)
    - password: the password of the new user (string, required)
    - email: the email of the new user (string, required)
    - first_name: the first name of the new user (string, optional)
    - last_name: the last name of the new user (string, optional)

    Returns a JSON response with the data of the newly created user, including its unique identifier in the system.

    Requires the requesting user to be authenticated and have admin privileges.
    """
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer
