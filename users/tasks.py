from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone


@shared_task
def deactivate_inactive_users():
    User = get_user_model()

    one_month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        is_active=True,
        last_login__lt=one_month_ago
    )

    count = inactive_users.update(is_active=False)

    return f'Deactivated {count} users'