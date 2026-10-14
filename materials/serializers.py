from rest_framework import serializers
from .models import Course, Lesson
from django.contrib.auth import get_user_model   # <-- правильный способ

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()   # доп. поле

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Не включай password в вывод!
        exclude = ('password',)

    def create(self, validated_data):
        # Важно: пароль нужно хешировать
        user = User.objects.create_user(**validated_data)
        return user