
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# urls
urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/auth/', include('authentication.urls')),  # include authentication app urls
    path('api/v1/', include('movies.urls')),  # include movies app urls

    # for API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]