from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import RegisterSerializer, LoginSerializer, UserDetailsSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.contrib.auth.hashers import make_password


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        password2 = request.data.get("password2")
        email = request.data.get("email")
        username = request.data.get("username")

        if not username:
            context = {
                'data': None,
                'message': 'Username is Not Given',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        if not email:
            context = {
                'data': None,
                'message': 'Email is Not Given',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )
        if not password:
            context = {
                'data': None,
                'message': 'Password is not Given',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        if not password2:
            context = {
                'data': None,
                'message': 'Password2 is not Given',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        password = request.data.pop("password")
        password2 = request.data.pop("password2")

        email_exist = User.objects.filter(email=email).exists()

        if email_exist:
            context = {
                'data': None,
                'message': 'Email is Already Found',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        username_exist = User.objects.filter(username=username).exists()

        if username_exist:
            context = {
                'data': None,
                'message': 'Username is Already Used',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        if not password == password2:
            context = {
                'data': None,
                'message': 'Password and Password2 is Not Matching',
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )
        try:
            password = make_password(password=password)
            user = User.objects.create(
                password=password,
                **request.data
            )

        except Exception as err:

            context = {
                'data': None,
                'message': "Account Can't Create",
                'error': True, 'code': 400,
            }
            return Response(
                context, status=400
            )

        serializer = LoginSerializer(instance=user)

        context = {
            'data': serializer.data,
            'message': 'Success',
            'error': False, 'code': 200,
        }
        return Response(
            context, status=200
        )

        return ResponseWrapper(data=context, status=200)


class UserProfileViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes =  (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        qs = User.objects.filter(username=self.request.user).last()

        if not qs:
            context = {
                'message': 'User Account is Not Found',
                'error': True, 'code': 400,
            }
            return Response(context, status=400)

        serializer = UserDetailsSerializer(instance=qs)

        context = {
            'data': serializer.data,
            'message': 'Success',
            'error': False, 'code': 200,
        }
        return Response(
            context, status=200
        )


class LoginViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        qs = User.objects.filter(Q(username=username)| Q(email=username)
                                        ).last()
        if not qs:
            context = {
                'message': 'Username is Not Valid',
                'error': True, 'code': 400,
                }
            return Response(context, status=400)

        elif qs.check_password(password):
            serializer = LoginSerializer(instance=qs)
            context = {
                'data': serializer.data,
                'message': 'Success',
                'error': False, 'code': 200,
            }
            return Response(
                context, status=200
            )

        context = {
                'message': 'Password is Not Valid',
                'error': True, 'code': 400,
            }

        return Response(context, status=400)
