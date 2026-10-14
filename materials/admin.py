from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at'] if 'created_at' in [f.name for f in Course._meta.get_fields()] else ['title']
    search_fields = ['title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['title', 'course__title']