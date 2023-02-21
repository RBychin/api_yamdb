from rest_framework import permissions

from api_yamdb.settings import ALLOWED_ROLES


class IsAuthorStaffOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.role in ALLOWED_ROLES)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif (request.user and request.user.admin_client):
            return True
