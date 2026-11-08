from django.conf import settings
from django.db import models

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
    )
    course = models.ForeignKey(
        'materials.Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} — {self.course}'

class Course(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(  # ← новое поле
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='Цена курса',
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    # Оставляем только ОДИН ForeignKey
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True,  # временно
        blank=True
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    preview = models.ImageField(upload_to='lessons/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)  # лучше добавить null=True, если ссылка может отсутствовать

    def __str__(self):
        # Хороший вариант: показывать и курс, и урок
        return f"{self.course.title} — {self.title}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('canceled', 'Отменён'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь',
    )
    paid_course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Оплаченный курс',
    )
    paid_lesson = models.ForeignKey(
        'Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный урок',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты',
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='transfer',
        verbose_name='Способ оплаты',
    )
    stripe_session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Session ID',
    )
    payment_url = models.URLField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату',
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Статус',
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты',
    )

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']

    def __str__(self):
        return f'{self.user} — {self.paid_course} — {self.status}'

