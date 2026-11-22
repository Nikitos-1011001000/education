from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверяет, состоит ли пользователь в группе 'moderator' (на уровне действия)."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='moderator').exists()


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Проверяет владельца объекта либо права модератора (на уровне объекта).
    owner/author — выбирай то поле, которое у тебя реально в модели.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        # Модератор: разрешает GET/PUT/PATCH
        if user.groups.filter(name='moderator').exists():
            if request.method in ['GET', 'PUT', 'PATCH']:
                return True

        # Владелец: проверяем по полю owner (или author — подставь своё)
        if hasattr(obj, 'owner') and obj.owner == user:
            return True
        if hasattr(obj, 'author') and obj.author == user:
            return True

        return False

class IsOwner(permissions.BasePermission):
    """
    Полный доступ к объекту только у владельца.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and obj.owner == request.user
        )