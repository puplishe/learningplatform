from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product
from lesson.models import LessonView, Lesson
from users.models import UserProfle
from datetime import datetime
class ProductStatsViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test data (products, lessons, lesson views, user profiles)
        self.product = Product.objects.create(name='Test Product', owner=self.user)
        self.lesson = Lesson.objects.create(name='Test Lesson', duration_seconds=120)
        self.lesson.products.add(self.product)  # Associate the product with the lesson
        start_time = datetime.fromisoformat('2023-09-23T10:00:00+00:00')
        end_time = datetime.fromisoformat('2023-09-23T10:30:00+00:00')

        self.lesson_view = LessonView.objects.create(
            user=self.user,
            lesson=self.lesson,
            start_time=start_time,
            end_time=end_time
        )
        self.user_profile = UserProfle.objects.create(user=self.user)
        self.user_profile.product_access.add(self.product)  # Grant access to the product for the user

        # Create additional users (non-product purchasers) and their user profiles
        self.user2 = User.objects.create_user(username='testuser2', password='testpassword2')
        self.user3 = User.objects.create_user(username='testuser3', password='testpassword3')

        self.lesson_view2 = LessonView.objects.create(
            user=self.user2,
            lesson=self.lesson,
            start_time=None,
            end_time=None
        )
        self.lesson_view3 = LessonView.objects.create(
            user=self.user3,
            lesson=self.lesson,
            start_time=start_time,
            end_time=end_time
        )

        self.user_profile2 = UserProfle.objects.create(user=self.user2)
        self.user_profile3 = UserProfle.objects.create(user=self.user3)

    def test_product_stats_view(self):
        # Create a test client
        client = APIClient()
        client.force_authenticate(user=self.user)  # Authenticate the user

        # Define the URL for the product stats endpoint
        url = reverse('product-list')

        # Make a GET request to the endpoint
        response = client.get(url)

        # Check the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the response data (assuming it's a list of product stats)
        data = response.data[0]  # Assuming the response is a list of product stats
        print(data)
        self.assertEqual(data['product_id'], self.product.id)
        self.assertEqual(data['product_name'], self.product.name)
        # Add more assertions to check other fields in the response data

    def tearDown(self):
        # Clean up test data (optional)
        self.user.delete()
        self.product.delete()
        self.lesson.delete()
        self.lesson_view.delete()
        self.user_profile.delete()

        # Clean up additional test data (non-product purchasers)
        self.user2.delete()
        self.user3.delete()
        self.lesson_view2.delete()
        self.lesson_view3.delete()
        self.user_profile2.delete()
        self.user_profile3.delete()