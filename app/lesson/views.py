from django.shortcuts import get_object_or_404
from product.models import Product
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from users.models import UserProfle

from .models import Lesson, LessonView
from .serializers import (
    CustomLessonSerializer,
    LessonCreateSerializer,
    SpecificProducSerializer,
)
from .utils import view_count_time


class LessonListView(generics.ListAPIView):

    serializer_class = CustomLessonSerializer

    def get(self, request, *args, **kwargs) -> list[dict[str, int | str | str | int]]:
        """
        Просмотр списка доступных для вас уроков.

        Эта функция позволяет вам увидеть все уроки, к которым у вас есть доступ, на основе
        продуктов, которые вы приобрели. Она предоставляет информацию о каждом уроке,
        включая его ID, название, статус (Завершен/Не завершен) и общее время просмотра в секундах.
        Пользователь должен быть зарегестрирован, чтобы увидеть уроки, к которым он имеет доступ.

        - **ID**: Уникальный идентификатор урока.
        - **Название**: Название урока.
        - **Статус**: Указывает, завершен ли урок или нет.
        - **Время просмотра**: Общее время, которое вы провели, просматривая урок, в секундах.

        **Responses**

        - 200 (Succsess): Вы получите список деталей уроков.
        """
        if request.user.is_anonymous:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = self.request.user

        try:
            user_profile = UserProfle.objects.get(user=user)
        except UserProfle.DoesNotExist:
            return Response(
                {'detail': 'User profile not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

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
        serializer = CustomLessonSerializer(lesson_data, many=True)
        return Response(serializer.data)


class LessonDetailView(generics.ListAPIView):

    serializer_class = SpecificProducSerializer

    def get(self, request, *args, **kwargs) -> list[dict[str, int | str | str | int]]:
        """
        Просмотр уроков для конкретного продукта, который вы приобрели.

        С этой функцией вы можете исследовать уроки, связанные с конкретным продуктом,
        который вы купили. Она предоставляет информацию о каждом уроке, включая его ID,
        название, статус (Завершен/Не завершен), общее время просмотра в секундах и метку времени
        вашего последнего просмотра. Точно так же пользователь должен быть зарегистрирован.

        - **ID**: Уникальный идентификатор урока.
        - **Название**: Название урока.
        - **Статус**: Указывает, завершен ли урок или нет.
        - **Время просмотра**: Общее время, которое вы провели, просматривая урок, в секундах.
        - **Последний просмотр**: Время вашего последнего просмотра этого урока.

        **Responses**

        - 200 (Sucsesful): Вы получите список деталей уроков.
        """
        if request.user.is_anonymous:
            return Response(
                {'detail': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user = self.request.user
        product_id = self.kwargs['product_id']

        has_purchased = UserProfle.objects.filter(user=user, product_access__id=product_id).exists()
        if not has_purchased:
            return Response(
                {'detail': 'No such product exist or you did not purchase such product'},
            )

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
        serializer = SpecificProducSerializer(lesson_data, many=True)
        return Response(serializer.data)


class LessonCreateView(generics.CreateAPIView):
    """
    Создание урока
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
