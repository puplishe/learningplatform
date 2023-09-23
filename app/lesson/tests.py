from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Product, Lesson, LessonView
import json
from users.models import UserProfle
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

class LessonListViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data (products, lessons)
        self.product1 = Product.objects.create(name='Product 1', owner=self.user)
        self.product2 = Product.objects.create(name='Product 2', owner=self.user)

        self.lesson1 = Lesson.objects.create(name='Lesson 1', duration_seconds=120)
        self.lesson1.products.add(self.product1)

        self.lesson2 = Lesson.objects.create(name='Lesson 2', duration_seconds=1800)
        self.lesson2.products.add(self.product2)

        # Create a user profile and grant access to products
        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product1)
        self.user_profile.product_access.add(self.product2)
        start_time = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time = datetime.fromisoformat('2023-09-23T10:10:00+00:00')
        # Create LessonView records for lessons with varying watched times
        self.lesson_view1 = LessonView.objects.create(user=self.user, lesson=self.lesson1, start_time=start_time, end_time=end_time, status=False)
        self.lesson_view2 = LessonView.objects.create(user=self.user, lesson=self.lesson2, start_time=start_time, end_time=end_time, status=False)

    def test_lesson_list_view_for_specific_user(self):
        # Create a test client
        client = APIClient()
        client.force_authenticate(user=self.user)  # Authenticate the user

        # Define the URL for the lesson list endpoint with a specific user_id
        user_id = self.user.id  # Get the user's ID
        url = reverse('lesson-list')

        # Make a GET request to the endpoint
        response = client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that both lessons are in the response data
        response_data = response.data
        self.assertEqual(len(response_data), 2)

        # Verify that the response data contains the expected fields (id, title, status, viewing_time)
        for lesson_data in response_data:
            self.assertIn('id', lesson_data)
            self.assertIn('title', lesson_data)
            self.assertIn('status', lesson_data)
            self.assertIn('viewing_time', lesson_data)

            # Check that status is either 'Completed' or 'Not Completed'
            self.assertIn(lesson_data['status'], ['Completed', 'Not Completed'])

            # Check that viewing_time is an integer
            self.assertIsInstance(lesson_data['viewing_time'], int)





class LessonDetailViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data (products, lessons)
        self.product1 = Product.objects.create(name='Product 1', owner=self.user)
        self.product2 = Product.objects.create(name='Product 2', owner=self.user)

        self.lesson1 = Lesson.objects.create(name='Lesson 1', duration_seconds=120)
        self.lesson1.products.add(self.product1)

        self.lesson2 = Lesson.objects.create(name='Lesson 2', duration_seconds=1800)
        self.lesson2.products.add(self.product1)

        # Create a user profile and grant access to products
        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product1)
        self.user_profile.product_access.add(self.product2)

        # Create LessonView records for lessons that are not watched over 80%
        start_time = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time = datetime.fromisoformat('2023-09-23T10:10:00+00:00')
        self.lesson_view1 = LessonView.objects.create(user=self.user, lesson=self.lesson1, start_time=start_time, end_time=end_time, status=False)
        self.lesson_view2 = LessonView.objects.create(user=self.user, lesson=self.lesson2, start_time=start_time, end_time=end_time, status=False)

    def test_lesson_detail_view_for_specific_product(self):
        # Create a test client
        client = APIClient()
        client.force_authenticate(user=self.user)  # Authenticate the user

        # Define the URL for the lesson detail endpoint with a specific product_id
        product_id = self.product1.id  # Choose one of the products
        url = reverse('lesson-detail', kwargs={'product_id': product_id})

        # Make a GET request to the endpoint
        response = client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that both lessons for the chosen product are in the response data
        response_data = response.data

        # Verify that the response data contains the expected fields (status, viewing_time, last_viewed, etc.)
        # You can add more specific assertions based on your serializer and data structure

        # Example assertion for the first lesson in the response
        for lesson_data in response_data:
            print(lesson_data)
            self.assertIn('id', lesson_data)
            self.assertIn('title', lesson_data)
            self.assertIn('status', lesson_data)
            self.assertIn('viewing_time', lesson_data)
            self.assertIn('last_viewed', lesson_data)
            self.assertEqual(lesson_data['last_viewed'], '2023-09-23 10:10:00')
        self.assertEqual(response_data[0]['status'], 'Completed')
        self.assertEqual(response_data[1]['status'], 'Not Completed')