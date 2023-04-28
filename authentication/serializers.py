from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        read_only=False, required=True, validators=[validate_password],
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    password2 = serializers.CharField(
        read_only=False, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] == attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT Custom Token Claims Serializer
    """

    # @staticmethod
    # def validate_email_verification_status(user):
    #     from allauth.account import app_settings
    #
    #     if (
    #             app_settings.EMAIL_VERIFICATION
    #             == app_settings.EmailVerificationMethod.MANDATORY
    #             and not user.emailaddress_set.filter(
    #         email=user.email, verified=True
    #     ).exists()
    #     ):
    #         raise serializers.ValidationError(_("E-mail is not verified."))

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # cls.validate_email_verification_status(user)
        # Add custom claims
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff

        return token
