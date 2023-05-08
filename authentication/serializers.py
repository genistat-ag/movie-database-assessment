from django.db.models import Q
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

    # we just store password, not expose to user so it should be write only
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password],
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    
    # password2 just for password validation, it should be write only
    password2 = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        # this is error because if password is equal then it is correct
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

class JwtAuthenticationSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        username = attrs.get('username')
        user = User.objects.filter(Q(username=username) | Q(email=username)).first()
        if user:
            credentials['username'] = user.username
        return super().validate(credentials)
