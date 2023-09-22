from django.db import models
from django.contrib.auth.models import User
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
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} -> {self.lesson.title}"

    def calculate_view_status(self):
        lesson_duration = self.lesson.duration_seconds
        viewed_duration = (self.end_time - self.start_time).total_seconds()
        
        if lesson_duration > 0 and (viewed_duration / lesson_duration) >= 0.8:
            self.status = True
        else:
            self.status = False

    def save(self, *args, **kwargs):
        self.calculate_view_status()
        super().save(*args, **kwargs)