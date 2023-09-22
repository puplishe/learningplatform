from django.shortcuts import render, get_object_or_404
from .models import LessonView, Lesson
from django.http import JsonResponse
from .models import LessonView, Lesson
from rest_framework.response import Response
import json
from .serializers import LessonSerializer
from rest_framework import generics, status
from product.models import Product
from users.models import UserProfle
from django.contrib.auth.models import User
def view_lesson(request, lesson_id):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        start_time = data["start_time"]
        end_time = data["end_time"]

        lesson = get_object_or_404(Lesson, pk=lesson_id)
        user = request.user

        # Filter UserProfle objects based on the user
        user_profile = get_object_or_404(UserProfle, user=user)

        # Check if the user has purchased the product associated with the lesson
        has_purchased = user_profile.product_access.filter(pk=lesson.product_id).exists()

        if not has_purchased:
            return JsonResponse({"message": "You have not purchased this product."}, status=403)

        # Calculate view status
        lesson_duration = lesson.duration_seconds
        
        if lesson_duration > 0 and start_time is not None and end_time is not None:
            viewed_duration = (end_time - start_time).total_seconds()
            percentage_viewed = (viewed_duration / lesson_duration) * 100

            if percentage_viewed >= 80:
                status = True
            else:
                status = False
        else:
            # Handle the case where lesson_duration is zero or negative
            status = False

        # Create a LessonView object and set the calculated status
        lesson_view = LessonView(user=user, lesson=lesson, start_time=start_time, end_time=end_time, status=status)
        lesson_view.save()

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
        
        # Ensure that the user has purchased the product before retrieving lessons
        has_purchased = UserProfle.objects.filter(user=user, product_access__id=product_id).exists()
        if not has_purchased:
            # Return an empty queryset or raise a permission error as needed
            return Lesson.objects.none()
        
        product = get_object_or_404(Product, id=product_id)
        return Lesson.objects.filter(products=product)
    
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id, users=user)
        
        # Ensure that the user has purchased the product before recording the lesson view
        has_purchased = User.objects.filter(userprofle__product_access=product)
        if not has_purchased:
            return Response({"message": "You have not purchased this product."}, status=status.HTTP_403_FORBIDDEN)
        
        # Your logic for recording the lesson view here...
        
        return Response({"message": "Lesson view recorded."}, status=status.HTTP_200_OK)