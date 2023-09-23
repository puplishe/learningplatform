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
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.product1, self.product2 = self.create_products()
        self.lesson1_1, self.lesson1_2, self.lesson2_1, self.lesson2_2 = self.create_lessons()

        self.user2, self.user3, self.user4, self.user5 = self.create_users()
        self.user_profile2, self.user_profile3, self.user_profile4, self.user_profile5 = self.create_user_profiles()

        self.grant_lesson_access()

    def create_products(self):
        product1 = Product.objects.create(name='Product 1', owner=self.user)
        product2 = Product.objects.create(name='Product 2', owner=self.user)
        return product1, product2

    def create_lessons(self):
        lesson1_1 = Lesson.objects.create(name='Lesson 1.1', duration_seconds=120)
        lesson1_2 = Lesson.objects.create(name='Lesson 1.2', duration_seconds=180)
        lesson2_1 = Lesson.objects.create(name='Lesson 2.1', duration_seconds=150)
        lesson2_2 = Lesson.objects.create(name='Lesson 2.2', duration_seconds=90)
        lesson1_1.products.add(self.product1)
        lesson1_2.products.add(self.product1)
        lesson2_1.products.add(self.product2)
        lesson2_2.products.add(self.product2)
        return lesson1_1, lesson1_2, lesson2_1, lesson2_2

    def create_users(self):
        user2 = User.objects.create_user(username='purchased_user1', password='testpassword2')
        user3 = User.objects.create_user(username='purchased_user2', password='testpassword3')
        user4 = User.objects.create_user(username='purchased_user3', password='testpassword4')
        user5 = User.objects.create_user(username='purchased_user4', password='testpassword5')
        return user2, user3, user4, user5

    def create_user_profiles(self):
        user_profile2 = UserProfle.objects.create(user=self.user2)
        user_profile3 = UserProfle.objects.create(user=self.user3)
        user_profile4 = UserProfle.objects.create(user=self.user4)
        user_profile5 = UserProfle.objects.create(user=self.user5)
        return user_profile2, user_profile3, user_profile4, user_profile5

    def grant_lesson_access(self):
        LessonView.objects.create(
            user=self.user2,
            lesson=self.lesson1_1,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user2,
            lesson=self.lesson1_2,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user3,
            lesson=self.lesson1_1,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user3,
            lesson=self.lesson1_2,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user4,
            lesson=self.lesson2_1,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user4,
            lesson=self.lesson2_2,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user5,
            lesson=self.lesson2_1,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )
        LessonView.objects.create(
            user=self.user5,
            lesson=self.lesson2_2,
            start_time=datetime.fromisoformat('2023-09-23T10:00:00+00:00'),
            end_time=datetime.fromisoformat('2023-09-23T10:20:00+00:00'),
        )

        self.user_profile2.product_access.add(self.product1)
        self.user_profile3.product_access.add(self.product1)
        self.user_profile4.product_access.add(self.product2)
        self.user_profile5.product_access.add(self.product2)

    def test_product_stats_view(self):
       
        client = APIClient()
        client.force_authenticate(user=self.user)  

        
        url = reverse('product-list')

        
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

       
        data = response.data  
        
        for item in data:
            print(item)
            self.assertIn(item['product_id'], [self.product1.id, self.product2.id])
            self.assertIn(item['product_name'], [self.product1.name, self.product2.name])
        

 