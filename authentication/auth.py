from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameLogin(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        Model = get_user_model()

        try:
            user = Model.objects.get(Q(username=username) | Q(email=username))
        except Model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None
