from datetime import timedelta

from django.contrib.auth.models import User
from lesson.models import LessonView
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Product
from .serializers import ProductCreateSerializer, ProductSerializer


class ProductStatsView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request) -> Response:
        """
        Получение статистики по продуктам.

        Это представление возвращает статистику для каждого продукта, включая общее количество просмотров,
        общее время просмотра, общее количество студентов и процент покупки.

        - **product_id**: Уникальный идентификатор продукта.
        - **product_name**: Название продукта.
        - **total_views**: Общее количество просмотров продукта.
        - **total_view_time**: Общее время просмотра продукта в секундах.
        - **total_students**: Общее количество студентов, купивших продукт.
        - **purchase_percentage**: Процент студентов, купивших продукт.

        **Responses**

        - 200 (Success): Список статистики продуктов.
        """

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


class ProductCreateView(generics.CreateAPIView):
    """
    Создание Продукта
    """
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
