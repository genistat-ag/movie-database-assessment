
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="API Testing",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="mehedibappi34@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


# urls
urlpatterns = [
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/movies/', include('movies.urls')),
    path('admin/', admin.site.urls),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]