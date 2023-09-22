from django.urls import path
from . import views

urlpatterns = [
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:product_id>/', views.LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/create/<int:product_id>', views.LessonCreateView.as_view(), name='lesson-create')
]