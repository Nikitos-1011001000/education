from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsOwner, IsOwnerOrModerator

def is_moderator(user):
    """
    Проверяет, состоит ли пользователь в группе модераторов.
    """
    return (
        user.is_authenticated
        and user.groups.filter(name='moderator').exists()
    )


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD для курсов.

    Обычный пользователь работает только со своими курсами.
    Модератор видит и может редактировать все курсы,
    но удалять может только свои.
    """
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.all()

        if is_moderator(self.request.user):
            return queryset

        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """
    CRUD для уроков.

    Обычный пользователь работает только со своими уроками.
    Модератор видит и может редактировать все уроки,
    но удалять может только свои.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lesson.objects.all()

        if is_moderator(self.request.user):
            return queryset

        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)