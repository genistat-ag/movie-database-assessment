
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


# urls
urlpatterns = [
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/movies/', include('movies.urls')),
    path('admin/', admin.site.urls),

    # for API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redocs/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]