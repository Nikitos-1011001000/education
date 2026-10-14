from rest_framework import viewsets, generics, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        is_owner = obj == request.user
        is_admin = request.user.is_superuser
        return is_owner or is_admin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]

    # Опционально: по умолчанию показывать только своего, если не админ
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            # Обычный пользователь видит только себя
            return qs.filter(pk=self.request.user.pk)
        return qs

class CourseViewSet(viewsets.ModelViewSet):
    """Весь CRUD для курса одним классом."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(generics.ListCreateAPIView):
    """GET — список уроков, POST — создать урок."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE — один урок."""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
