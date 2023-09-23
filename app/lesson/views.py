from django.shortcuts import get_object_or_404
from .models import LessonView, Lesson
from .models import LessonView, Lesson
from rest_framework.response import Response
from .serializers import LessonStatusSerializer, CustomLessonSerializer, SpecificProducSerializer
from rest_framework import generics, status
from product.models import Product
from users.models import UserProfle
from django.contrib.auth.models import User
from typing import List, Dict, Union
from .utils import view_count_time

class LessonListView(generics.ListAPIView):
    serializer_class = CustomLessonSerializer

    def get_queryset(self) -> List[Dict[str, Union[int, str, str, int]]]:
        user = self.request.user

        try:
            user_profile = UserProfle.objects.get(user=user)
        except UserProfle.DoesNotExist:
            return Lesson.objects.none()

        product_ids = user_profile.product_access.values_list('id', flat=True)
        lessons = Lesson.objects.filter(products__id__in=product_ids).distinct()

        lesson_data = []

        for lesson in lessons:
            duration = lesson.duration_seconds
            lesson_view = LessonView.objects.select_for_update().filter(user=user, lesson=lesson).first()
            data = view_count_time(duration, lesson_view)
            
            lesson_view.save()
            lesson_data.append({
                'id': lesson.id,
                'title': lesson.name,
                'status': data.status,
                'viewing_time': data.time_watched,
            })

        return lesson_data

class LessonDetailView(generics.ListAPIView):
    serializer_class = SpecificProducSerializer

    def get_queryset(self) -> List[Dict[str, Union[int, str, str, int]]]:
        user = self.request.user
        product_id = self.kwargs['product_id']

        has_purchased = UserProfle.objects.filter(user=user, product_access__id=product_id).exists()
        if not has_purchased:
            return Lesson.objects.none()

        product = get_object_or_404(Product, id=product_id)
        lessons = Lesson.objects.filter(products=product)

        lesson_data = []

        for lesson in lessons:
            lesson_view = LessonView.objects.filter(user=user, lesson=lesson).order_by('-end_time').first()
            data = view_count_time(lesson.duration_seconds, lesson_view)
            data.save()
            print(data)
            lesson_data.append({
                'id': lesson.id,
                'title': lesson.name,
                'status': data.status,
                'viewing_time': int(data.time_watched),
                'last_viewed': data.end_time.strftime('%Y-%m-%d %H:%M:%S') if data.end_time else 'Not watched',
            })

        return lesson_data

class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonStatusSerializer

    def create(self, request, *args, **kwargs):
        user = self.request.user
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id, users=user)
        
        has_purchased = User.objects.filter(userprofle__product_access=product)
        if not has_purchased:
            return Response({"message": "You have not purchased this product."}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({"message": "Lesson view recorded."}, status=status.HTTP_200_OK)