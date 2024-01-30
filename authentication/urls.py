from django.urls import path
from authentication.views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import JwtAuthenticationSerializer

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(serializer_class=JwtAuthenticationSerializer), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
]