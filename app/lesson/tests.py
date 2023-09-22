from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Product, Lesson, LessonView
import json
from users.models import UserProfle
from datetime import datetime
from django.shortcuts import get_object_or_404

class ViewLessonTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data (products, lessons)
        self.product = Product.objects.create(name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', duration_seconds=120)
        self.lesson.products.add(self.product)  # Associate the product with the lesson
        
        # Create a user profile and grant access to the product
        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product)

    def test_view_lesson_detail_with_valid_data(self):
        # Create a test client
        client = APIClient()
        client.force_authenticate(user=self.user)  # Authenticate the user
        
        # Define the URL for the lesson detail endpoint
        url = reverse('lesson-detail', args=[self.product.id])  # Use the lesson ID

        # Create valid lesson view data

        # Make a POST request to the endpoint with valid data
        response = client.get(url)
        data = response.data[0]
        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], self.lesson.name)
        self.assertEqual(data['duration_seconds'], self.lesson.duration_seconds)


    # def test_view_lesson_detail_with_invalid_data(self):
    #     # Create a test client
    #     client = APIClient()
    #     client.force_authenticate(user=self.user)  # Authenticate the user

    #     # Define the URL for the lesson detail endpoint
    #     url = reverse('lesson-detail', args=[self.product.id])  # Use the product_id

    #     # Create invalid lesson view data (missing start_time)
    #     data = {
    #         "end_time": "2023-09-23T10:30:00+00:00"
    #     }

    #     # Make a POST request to the endpoint with invalid data
    #     response = client.post(url, data=json.dumps(data), content_type='application/json')

    #     # Check the response status code
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     # Check that the lesson view was not recorded
    #     lesson_view = LessonView.objects.filter(user=self.user, lesson=self.lesson).first()
    #     self.assertIsNone(lesson_view)

    # def test_view_lesson_create_with_valid_data(self):
    #     # Create a test client
    #     client = APIClient()
    #     client.force_authenticate(user=self.user)  # Authenticate the user

    #     # Define the URL for the lesson create endpoint
    #     url = reverse('lesson-create', args=[self.product.id])  # Use the product_id

    #     # Create valid lesson view data
    #     data = {
    #         "start_time": "2023-09-23T10:00:00+00:00",
    #         "end_time": "2023-09-23T10:30:00+00:00"
    #     }

    #     # Make a POST request to the endpoint with valid data
    #     response = client.post(url, data=json.dumps(data), content_type='application/json')

    #     # Check the response status code
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    #     # Check that the lesson view was recorded
    #     lesson_view = LessonView.objects.filter(user=self.user, lesson=self.lesson).first()
    #     self.assertIsNotNone(lesson_view)
    #     self.assertTrue(lesson_view.status)

    def tearDown(self):
        # Clean up test data
        self.user.delete()
        self.product.delete()
        self.lesson.delete()
        self.user_profile.delete()