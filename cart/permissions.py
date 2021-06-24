from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and str(obj.user).lower() == str(request.user.email).lower())


class IsCustomerPermission(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user:
                return bool(request.user.is_authenticated)
        except:
            return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
