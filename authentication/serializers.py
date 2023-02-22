from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class BaseTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):

        password = attrs.get("password")
        try: 
            user_obj = User.objects.get(Q(email=attrs.get("username"))|Q(username=attrs.get("username")))
            if user_obj is not None:
                credentials = {
                    'username':user_obj.username,
                    'password': password
                }
                if all(credentials.values()):
                    user = authenticate(**credentials)
                    if user:
                        if not user.is_active:
                            msg = _('User account is disabled.')
                            raise serializers.ValidationError(msg)

                        self.user = user

                        refresh = self.get_token(self.user)

                        data = {
                            'refresh': str(refresh),
                            'access' : str(refresh.access_token)
                        }

                        return data
                    else:
                        msg = _('Unable to log in with provided credentials.')
                        raise serializers.ValidationError(msg)

                else:
                    msg = _('Must include "{username_field}" and "password".')
                    msg = msg.format(username_field=self.username_field)
                    raise serializers.ValidationError(msg)
        except User.DoesNotExist:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        # if attrs['password'] == attrs['password2']:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user
