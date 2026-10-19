from rest_framework import serializers
from .models import Course, Lesson
from django.contrib.auth import get_user_model   # <-- правильный способ

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)# доп. поле

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
