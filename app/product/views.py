from rest_framework.response import Response
from rest_framework import generics
from .models import Product
from lesson.models import LessonView
from datetime import timedelta
import json
from .serializers import ProductSerializer
from django.contrib.auth.models import User
# Create your views here.
from typing import List, Dict, Union

class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request) -> Response:
        products = Product.objects.all()
        stats = []

        for product in products:
            users_with_access = User.objects.filter(userprofle__product_access=product)

            lesson_views = LessonView.objects.filter(user__in=users_with_access, lesson__products=product)

            total_views = lesson_views.count()
            total_view_time = timedelta()
            
            for lesson_view in lesson_views:
                if lesson_view.time_watched is None:
                    if lesson_view.start_time is not None and lesson_view.end_time is not None:
                        total_view_time += lesson_view.end_time - lesson_view.start_time
                else:
                    if lesson_view.start_time is not None and lesson_view.end_time is not None:
                        total_view_time += lesson_view.time_watched + lesson_view.end_time - lesson_view.start_time

            total_students = users_with_access.count()

            stats.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_views': total_views,
                'total_view_time': total_view_time.total_seconds(),
                'total_students': total_students,
                'purchase_percentage': (total_students / User.objects.count()) * 100,
            })

        serializer = ProductSerializer(stats, many=True)
        return Response(serializer.data)