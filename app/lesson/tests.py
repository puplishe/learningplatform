from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.models import UserProfle

from .models import Lesson, LessonView, Product


class LessonListViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.product1 = Product.objects.create(name='Product 1', owner=self.user)
        self.product2 = Product.objects.create(name='Product 2', owner=self.user)

        self.lesson1 = Lesson.objects.create(name='Lesson 1', duration_seconds=3600)
        self.lesson1.products.add(self.product1)

        self.lesson2 = Lesson.objects.create(name='Lesson 2', duration_seconds=120)
        self.lesson2.products.add(self.product2)

        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product1)
        self.user_profile.product_access.add(self.product2)
        start_time = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time = datetime.fromisoformat('2023-09-23T10:20:00+00:00')
        start_time2 = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time2 = datetime.fromisoformat('2023-09-23T10:01:00+00:00')

        self.lesson_view1 = LessonView.objects.create(
            user=self.user, lesson=self.lesson1, start_time=start_time, end_time=end_time, status=False)
        self.lesson_view2 = LessonView.objects.create(
            user=self.user, lesson=self.lesson2, start_time=start_time2, end_time=end_time2, status=False)

    def test_lesson_list_view_for_specific_user(self):

        client = APIClient()
        client.force_authenticate(user=self.user)

        url = reverse('lesson-list')

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertEqual(len(response_data), 2)

        for lesson_data in response_data:
            self.assertIn('id', lesson_data)
            self.assertIn('title', lesson_data)
            self.assertIn('status', lesson_data)
            self.assertIn('viewing_time', lesson_data)

            self.assertIn(lesson_data['status'], ['True', 'False'])

            self.assertIsInstance(lesson_data['viewing_time'], int)


class LessonDetailViewTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.product1 = Product.objects.create(name='Product 1', owner=self.user)
        self.product2 = Product.objects.create(name='Product 2', owner=self.user)

        self.lesson1 = Lesson.objects.create(name='Lesson 1', duration_seconds=120)
        self.lesson1.products.add(self.product1)

        self.lesson2 = Lesson.objects.create(name='Lesson 2', duration_seconds=2800)
        self.lesson2.products.add(self.product1)

        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product1)
        self.user_profile.product_access.add(self.product2)

        start_time = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time = datetime.fromisoformat('2023-09-23T10:10:00+00:00')
        start_time2 = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time2 = datetime.fromisoformat('2023-09-23T10:30:00+00:00')
        self.lesson_view1 = LessonView.objects.create(
            user=self.user, lesson=self.lesson1, start_time=start_time, end_time=end_time, status=False)
        self.lesson_view2 = LessonView.objects.create(
            user=self.user, lesson=self.lesson2, start_time=start_time2, end_time=end_time2, status=False)

    def test_lesson_detail_view_for_specific_product(self):

        client = APIClient()
        client.force_authenticate(user=self.user)

        product_id = self.product1.id
        url = reverse('lesson-detail', kwargs={'product_id': product_id})

        response = client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data

        for lesson_data in response_data:

            self.assertIn('id', lesson_data)
            self.assertIn('title', lesson_data)
            self.assertIn('status', lesson_data)
            self.assertIn('viewing_time', lesson_data)
            self.assertIn('last_viewed', lesson_data)
        self.assertEqual(response_data[0]['last_viewed'], '2023-09-23 10:10:00')
        self.assertEqual(response_data[1]['last_viewed'], '2023-09-23 10:30:00')
        self.assertEqual(response_data[0]['status'], 'True')
        self.assertEqual(response_data[1]['status'], 'False')
