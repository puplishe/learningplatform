from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from product.models import Product


class Lesson(models.Model):
    name = models.CharField(max_length=255, default='Default Lesson Name')
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.PositiveIntegerField()
    products = models.ManyToManyField(Product, related_name='lesson')

    def __str__(self):
        return self.title


class LessonView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    status = models.BooleanField(default=False)
    time_watched = models.FloatField(null=True)

    def __str__(self):
        return f'{self.user.username} -> {self.lesson.title}'
