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
        if hasattr(obj, "creator"):
            return obj.creator == request.user

        # Write permissions are only allowed to the creator of the rating
        if hasattr(obj, "reviewer"):
            return obj.reviewer == request.user


class HasMoviePermission(permissions.BasePermission):
    """
    Custom permission to only allow creator of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        # allow the authenticated user create report
        if view.action in ['create']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # no one can update report object
        if view.action in ['update', 'partial_update']:
            return False

        # superuser has all permission
        if request.user.is_superuser:
            return True

        return False
