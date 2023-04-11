from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        # Feature Fix: Here setting `write_only=True` as it's best practice 
        # to not share any password or secrets releted items in API response
        read_only=False, write_only=True, required=True, validators=[validate_password], 
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    """
    Bug Fix:
    ============================
    Here setting the `write_only=True` due to `User` model dosen't have any
    `password2` field/attribute as it saves the data to database but throws an exception
    With `write_only=True` it only takes the argument on request time.
    """
    password2 = serializers.CharField(
        read_only=False, write_only=True, required=True, style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2', None)
        """
        Bug Fix:
        ============================
        Here previously a bug was there it was checking if `password` and `password2` are same 
        then it's raising validation error. But it should be same.
        Also Removing the password2 attribute from here so that in `create` method can be much 
        shorter and cleaner. MUCH Cleaner Also.
        """
        if password2 is None:
            raise serializers.ValidationError({"password": "Password2 field required !"})
        if password != password2:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


    def create(self, validated_data):
        """
        Feature Fix:
        ============================
        Previously here there was around 4 lines of code for a simple user create.
        Now as the `password2` field is already removed in `validate` function we can
        now ommit that part. Also we don't have to manually use the `set_password` function
        as `create_user` does that already for us.
        """
        user = User.objects.create_user(**validated_data)
        return user
