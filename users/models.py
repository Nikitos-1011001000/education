from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None   # отключаем стандартный логин

    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'          # ← вход по email
    REQUIRED_FIELDS = []
