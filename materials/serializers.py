from rest_framework import serializers
from .models import Course, Lesson
from django.contrib.auth import get_user_model   # <-- правильный способ

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="email",
        read_only=True,
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "owner",
            "course",
            "title",
            "description",
            "preview",
            "video",
        ]


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="email",
        read_only=True,
    )
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)# доп. поле

    class Meta:
        model = Course
        fields = [
            "id",
            "owner",
            "title",
            "preview",
            "description",
            "lessons_count",
            "lessons",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
