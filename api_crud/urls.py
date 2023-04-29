from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Movie Database API",
        default_version="0.0.1",
        description="This is the assessment project for Movie Database API.",
        terms_of_service="https://www.django-rest-framework.org/",
        contact=openapi.Contact(email="abdur.rakib.1508@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    permission_classes=[permissions.AllowAny],
    public=True,
)

# urls
urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # application routes
    path("api/v1/auth/", include("authentication.urls")),
    path("api/v1/movies/", include("movies.urls")),
    # API documentation routes
    re_path(r"^(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^$", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
