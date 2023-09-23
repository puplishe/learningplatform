from django.shortcuts import render, get_object_or_404
from .models import LessonView, Lesson
from django.http import JsonResponse
from .models import LessonView, Lesson
from rest_framework.response import Response
import json
from .serializers import LessonStatusSerializer, CustomLessonSerializer, SpecificProducSerializer
from rest_framework import generics, status
from product.models import Product
from users.models import UserProfle
from django.contrib.auth.models import User
from django.db.models import Subquery, OuterRef, Sum, IntegerField, Case, When, Value, F, CharField
from datetime import timedelta
from django.db.models import F, Sum, ExpressionWrapper, DurationField
from django.utils import timezone



class LessonListView(generics.ListAPIView):
    serializer_class = CustomLessonSerializer

    def get_queryset(self):
        user = self.request.user

        # Get the user's profile
        try:
            user_profile = UserProfle.objects.get(user=user)
        except UserProfle.DoesNotExist:
            return Lesson.objects.none()

        # Retrieve all product IDs that the user has access to through the profile
        product_ids = user_profile.product_access.values_list('id', flat=True)

        # Retrieve all lessons for the user across all products
        lessons = Lesson.objects.filter(products__id__in=product_ids).distinct()

        lesson_data = []  # List to store lesson data

        # Calculate viewing_time and status for each lesson
        for lesson in lessons:
            lesson_view = LessonView.objects.filter(user=user, lesson=lesson).first()
            if lesson_view:
                lesson_duration_seconds = lesson.duration_seconds
                if lesson_duration_seconds:
                    if lesson_view.start_time is not None and lesson_view.end_time is not None:
                        viewing_time_seconds = (lesson_view.end_time - lesson_view.start_time).total_seconds()
                        if viewing_time_seconds >= 0.8 * lesson_duration_seconds:
                            status = 'Completed'
                        else:
                            status = 'Not Completed'
                    else:
                        status = 'Not Completed'
                else:
                    status = 'Not Completed'
                viewing_time = int(viewing_time_seconds) if 'viewing_time_seconds' in locals() else 0
            else:
                status = 'Not Completed'
                viewing_time = 0
            
            lesson_data.append({
                'id': lesson.id,
                'title': lesson.name,
                'status': status,
                'viewing_time': viewing_time,
            })

        return lesson_data
    
class LessonDetailView(generics.ListAPIView):
    serializer_class = SpecificProducSerializer

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id']

        # Ensure that the user has purchased the product before retrieving lessons
        has_purchased = UserProfle.objects.filter(user=user, product_access__id=product_id).exists()
        if not has_purchased:
            # Return an empty queryset or raise a permission error as needed
            return Lesson.objects.none()

        product = get_object_or_404(Product, id=product_id)

        # Retrieve all lessons for the product
        lessons = Lesson.objects.filter(products=product)

        lesson_data = []  # Create a list to store lesson data

        # Calculate viewing_time, status, and last_viewed for each lesson
        for lesson in lessons:
            lesson_view = LessonView.objects.filter(user=user, lesson=lesson).order_by('-end_time').first()
            if lesson_view:
                lesson_duration_seconds = lesson.duration_seconds
                if lesson_duration_seconds:
                    if lesson_view.start_time is not None and lesson_view.end_time is not None:
                        viewing_time_seconds = (lesson_view.end_time - lesson_view.start_time).total_seconds()
                        if viewing_time_seconds >= 0.8 * lesson_duration_seconds:
                            status = 'Completed'
                        else:
                            status = 'Not Completed'
                    else:
                        status = 'Not Completed'
                else:
                    status = 'Not Completed'

                last_viewed = lesson_view.end_time  # Get the end time as the last viewed time
            else:
                status = 'Not Completed'
                last_viewed = None  # No views for this lesson

            # Append lesson data to the list
            lesson_data.append({
                'id': lesson.id,
                'title': lesson.name,
                'status': status,
                'viewing_time': int(viewing_time_seconds) if status == 'Completed' else 0,
                'last_viewed': last_viewed.strftime('%Y-%m-%d %H:%M:%S') if last_viewed else None,
            })

        return lesson_data  # Return the list of lesson data
    
class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonStatusSerializer

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