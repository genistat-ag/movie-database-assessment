from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.db.models import Q

User = get_user_model()


class EmailUsernameAuthenticationBackend(object):
    """
    custom authentication backend for email or username and password authentication
    validate user using email or username and password and return user
    """

    @staticmethod
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(Q(email=username) | Q(
                username=username), )  # get user using email or username and password filtering from database using Q

        except User.DoesNotExist:
            return None

        return user if user and check_password(password, user.password, ) else None


    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
