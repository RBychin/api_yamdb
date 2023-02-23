from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Доступ разрешен Администратору."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))
