from django.urls import path
from authentication.views import RegisterView, LoginViewSet, UserProfileViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/',LoginViewSet.as_view(), name='login'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('user_details/', UserProfileViewSet.as_view(), name='user_details'),
]