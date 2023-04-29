from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    password = serializers.CharField(
        read_only=False,
        required=True,
        validators=[validate_password],
        style={"input_type": "password", "placeholder": "Password"},
    )
    password2 = serializers.CharField(
        write_only=True,  # bug: password2 is not intended to be read, so write_only=True
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )

    class Meta:
        model = User
        fields = ("username", "password", "password2", "email", "first_name", "last_name")

    def validate(self, attrs):
        # bug: when password and password2 are same, it is showing error
        # if attrs["password"] == attrs["password2"]:
        #     raise serializers.ValidationError({"password": "Password fields didn't match."})

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        del validated_data["password2"]
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])
        user.save()

        return user
