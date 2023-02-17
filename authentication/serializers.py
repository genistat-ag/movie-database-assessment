from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer, PasswordField
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.settings import api_settings
import importlib
rule_package, user_eligible_for_login = api_settings.USER_AUTHENTICATION_RULE.rsplit('.', 1)
login_rule = importlib.import_module(rule_package)

from rest_framework import exceptions



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],  # bug 2
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}  # bug 3
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        # bug 4
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


class EmailTokenObtainSerializer(TokenObtainSerializer):
    username_field = User.USERNAME_FIELD
    useremail_field = User.EMAIL_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(required=False)
        self.fields[self.useremail_field] = serializers.EmailField(required=False)
        self.fields['password'] = PasswordField()


    def validate(self, attrs):
        if attrs.get('username')!=None:
            username = attrs.get('username')
        else:
            email = attrs.get('email')
            username = User.objects.get(email=email).username

        authenticate_kwargs = {
            self.username_field: username,
            'password': attrs['password'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not getattr(login_rule, user_eligible_for_login)(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}


class CustomTokenObtainPairSerializer(EmailTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        # print("USR", self.user)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
