from rest_framework import serializers
from .models import Lesson
from django.contrib.auth.models import AnonymousUser
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user

        if not isinstance(user, AnonymousUser):
            # Only include 'id' if the user is authenticated
            data['user_id'] = user.id

        return data