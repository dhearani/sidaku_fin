from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Detail

class IsUMKM(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the required role
        if not request.user.is_authenticated:
            return False

        try:
            profile = request.user.detail
        except Detail.DoesNotExist:
            return False

        return bool(profile.role == 'umkm')


class IsKoperasi(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the required role
        if not request.user.is_authenticated:
            return False

        try:
            profile = request.user.detail
        except Detail.DoesNotExist:
            return False

        return bool(profile.role == 'koperasi')
    
class IsAdminSI(BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the required role
        if not request.user.is_authenticated:
            return False

        try:
            profile = request.user.detail
        except Detail.DoesNotExist:
            return False

        return bool(profile.role == 'adminsi')
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
