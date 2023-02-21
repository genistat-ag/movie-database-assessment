from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions

# urls
urlpatterns = [
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/movies/', include('movies.urls')),
    path('admin/', admin.site.urls),
]
