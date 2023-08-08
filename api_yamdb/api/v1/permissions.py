from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAdminUser)


class IsSuperUser(IsAdminUser):
    """Доступ пользователя с правами не ниже Администратора."""

    def has_permission(self, request, view):
        return request.user.is_superuser


class SafeMethodsOrIsSuperUser(IsSuperUser):
    """Доступ от имени пользователей разршен только при безопастном
    запросе, создание объектов доступно пользователя с првами не
    ниже Администратора."""

    def has_permission(self, request, view):
        is_superuser = super().has_permission(request, view)
        return is_superuser or request.method in SAFE_METHODS


class OwnerAndGodsOrReadOnly(BasePermission):
    """Доступ от имени пользователей разршен только при безопастном
        запросе или аутентифицированным пользователям,
        создание объектов доступно авторам объектов или пользователям с првами
        не ниже Модератора."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_staff
            or request.user.is_superuser)
