
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from lesson.models import LessonView
from users.models import UserProfle
from datetime import timedelta
import json
from django.contrib.auth.models import User
# Create your views here.


class ProductStatsView(APIView):
    def get(self, request):
        products = Product.objects.all()
        stats = []

        for product in products:
            # Filter users who have purchased the product
            users_with_access = User.objects.filter(userprofle__product_access=product)
            lesson_views = LessonView.objects.filter(user__in=users_with_access, lesson__products=product)

            total_views = lesson_views.count()
            total_view_time = timedelta()

            for lesson_view in lesson_views:
                if lesson_view.start_time is not None and lesson_view.end_time is not None:
                    total_view_time += lesson_view.end_time - lesson_view.start_time

            total_students = User.objects.all().count()

            if total_students > 0:
                purchase_percentage = (product.users.count() / total_students) * 100
            else:
                purchase_percentage = 0

            stats.append({
                'product_id': product.id,
                'product_name': product.name,
                'total_views': total_views,
                'total_view_time': total_view_time.total_seconds(),
                'total_students': total_students,
                'purchase_percentage': purchase_percentage,
            })

        return Response(stats)