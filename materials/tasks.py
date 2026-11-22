from datetime import timedelta
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from .models import Course, Subscription


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return

    subscriptions = Subscription.objects.filter(
        course=course
    ).select_related('user')

    recipients = [
        subscription.user.email
        for subscription in subscriptions
        if subscription.user.email
    ]

    if not recipients:
        return

    send_mail(
        subject=f'Курс "{course.title}" обновлён',
        message=(
            f'В курсе "{course.title}" появились обновления.\n\n'
            f'Откройте курс, чтобы посмотреть новые материалы.'
        ),
        from_email=None,
        recipient_list=recipients,
        fail_silently=False,
    )