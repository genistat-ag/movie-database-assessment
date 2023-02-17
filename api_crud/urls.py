
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
#from django.conf.urls import url
from rest_framework import permissions
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi


schema_view = get_schema_view(
   openapi.Info(
    
      title="Movies",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@arabika.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

swagger_url = [
    path('api/swagger.json/',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger',
                                           cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
]


# urls
urlpatterns = [
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/movies/', include('movies.urls')),
    path('admin/', admin.site.urls),
]+swagger_url


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
