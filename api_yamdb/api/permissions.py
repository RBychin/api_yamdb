from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Доступ разрешен только автору объекта."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user == obj.author)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Администратору."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin'
                    or request.user.is_superuser)))

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.is_superuser)


class IsModeratorOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Модератору."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'moderator')


class IsUserOrReadOnly(permissions.BasePermission):
    """Доступ разрешен Пользователю (user)."""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'user')
