from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from product.models import Product

class UserProfle(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product_access = models.ManyToManyField(Product, related_name='users')

