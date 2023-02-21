from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the movie
        return obj.creator == request.user

class IsReviewerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the movie
        return obj.reviewer == request.user

class IsSuperuser(permissions.BasePermission):
    """ Superuser's permission """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

class IsSuperuserOrAuthenticatedForGetAndPost(permissions.BasePermission):
    """
    Superuser has GET permission, Rest has POST permission
    """
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        return bool(request.method == 'GET' and request.user.is_superuser)