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


class UserLogInTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom UserLogInTokenObtainPairSerializer to allow authentication using email or username"""

    def validate(self, attrs):
        credentials = {
            'username': attrs.get("username"),
            'password': attrs.get("password")
        }
        return super().validate(credentials)
