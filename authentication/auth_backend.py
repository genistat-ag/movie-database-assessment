"""
@create_by jibon


This module created due to the clause mentioned in Use Cases

As stated Users should be able to log in with both the below combinations
    - username and password
    - email and password

With below `MultiAttributeAuthBackend` we are overriding the in-built django 
ModelBackend for `User` model. We are using Q operator for checking if `username`
is matching with username or email field.
"""


from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class MultiAttributeAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            return None
        else:
            # Check if the password is correct
            if user.check_password(password):
                return user