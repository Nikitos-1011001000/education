from rest_framework import serializers
from .models import Course, Lesson, Subscription
from django.contrib.auth import get_user_model   # <-- правильный способ
from materials.validators import validate_youtube_link

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        validators=[validate_youtube_link],
        required=False,
        allow_null=True,
        allow_blank=True,
    )

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
            "video_link",
        ]


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="email",
        read_only=True,
    )
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)# доп. поле
    is_subscribed = serializers.SerializerMethodField()

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
            "is_subscribed",
        ]

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')

        if request is None or not request.user.is_authenticated:
            return False

        return Subscription.objects.filter(
            user=request.user,
            course=obj,
        ).exists()

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Subscription
        fields = '__all__'  # Или явно: ['id', 'user', 'plan', 'is_active', 'created_at']
