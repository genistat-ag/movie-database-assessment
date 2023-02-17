from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import JWTAuthentication as JWTA


class CustomJWTAuthentication(JWTA):
    pass



class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    name = "CustomJWTAuth"
    target_class = CustomJWTAuthentication