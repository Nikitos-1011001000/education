from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение на редактирование только владельцу объекта.
    Для просмотра — любой авторизованный пользователь.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) любому авторизованному
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для записи (PUT/PATCH/DELETE) — только если это его профиль
        return obj == request.user