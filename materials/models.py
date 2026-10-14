from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    # Оставляем только ОДИН ForeignKey
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
