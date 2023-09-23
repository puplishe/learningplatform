from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.ProductStatsView.as_view(), name='product-list'),
]
