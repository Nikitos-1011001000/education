from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from .permissions import IsOwner, IsOwnerOrModerator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.paginators import StandardPagination

class SubscriptionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if course_id is None:
            return Response(
                {'error': 'Не передан course_id'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(
            user=user,
            course=course_item,
        )

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(
                user=user,
                course=course_item,
            )
            message = 'подписка добавлена'

        return Response({'message': message})

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
    queryset = Course.objects.all()
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.all()

        if self.action in ('update', 'partial_update', 'destroy'):
            if not is_moderator(self.request.user):
                return queryset.filter(owner=self.request.user)

        return queryset


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

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = StandardPagination

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

class LessonCreateAPIView(APIView):  # или ListCreateAPIView и т.д.
    pass

class LessonDestroyAPIView(APIView):
    pass

class LessonListAPIView(APIView):
    pass

class LessonRetrieveAPIView(APIView):
    pass

class LessonUpdateAPIView(APIView):
    pass

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer