from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


User = get_user_model()


class UsernameOrEmailAuthenticationBackend(ModelBackend):
    """
    Responsible for Enabling Username or Email Login
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            User().set_password(password)
            return
        except User.MultipleObjectsReturned:
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
