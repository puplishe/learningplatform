from django.shortcuts import render, get_object_or_404
from .models import LessonView, Lesson
from django.http import JsonResponse
from .models import LessonView, Lesson
from django.utils import timezone
import json
from .serializers import LessonSerializer
from rest_framework import generics
from product.models import Product
def view_lesson(request, lesson_id):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        start_time = data["start_time"]
        end_time = data["end_time"]

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        user = request.user

        # Create a LessonView object to record the view.
        lesson_view = LessonView(user=user, lesson=lesson, start_time=start_time, end_time=end_time)
        lesson_view.save()  # This will also calculate and set the status

        return JsonResponse({"message": "Lesson view recorded."})

    return JsonResponse({"message": "Invalid request method."})




class LessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_ids = Product.objects.filter(users=user).values_list('id', flat=True)
        return Lesson.objects.filter(products__id__in=product_ids)
    
class LessonDetailView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id, users=user)
        return Lesson.objects.filter(products=product)