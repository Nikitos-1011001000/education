from django.contrib import admin
from .models import Course, Lesson, Payment, Subscription

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at'] if 'created_at' in [f.name for f in Course._meta.get_fields()] else ['title']
    search_fields = ['title']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    list_filter = ['course']
    search_fields = ['title', 'course__title']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'payment_date',
        'paid_course',
        'paid_lesson',
        'amount',
        'payment_method',
        'status',
    )
    list_filter = ('status', 'payment_method')
    search_fields = ('user__email',)