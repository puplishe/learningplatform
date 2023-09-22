from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from lesson.models import LessonView
from django.db.models import Count, Sum
from users.models import UserProfle
from datetime import timedelta
# Create your views here.


class ProductStatsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        stats = []

        for product in products:
            lesson_views = LessonView.objects.filter(lesson__products=product)
            total_views = lesson_views.count()
            total_view_time = timedelta()  # Initialize total view time as a timedelta

            for lesson_view in lesson_views:
                total_view_time += lesson_view.end_time - lesson_view.start_time

            total_students = UserProfle.objects.all().count()

            if total_students > 0:
                purchase_percentage = (product.users.count() / total_students) * 100
            else:
                purchase_percentage = 0

            stats.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_views': total_views,
                'total_view_time': total_view_time.total_seconds(),  # Convert timedelta to seconds
                'total_students': total_students,
                'purchase_percentage': purchase_percentage,
            })

        return Response(stats)