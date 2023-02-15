from rest_framework import permissions

from api_yamdb.settings import ALLOWED_ROLES


class IsAuthorStaffOrReadOnly(permissions.BasePermission):

    # def has_permission(self, request, view):
    #     return (request.method in permissions.SAFE_METHODS
    #             or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author
                or request.user.role in ALLOWED_ROLES)
