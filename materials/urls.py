from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateAPIView, LessonRetrieveUpdateDestroyAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),                        # /courses/...
    path('lessons/', LessonListCreateAPIView.as_view()),   # GET, POST
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view()),  # GET, PUT, DELETE
]