from rest_framework import serializers

from .models import Lesson


class LessonStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CustomLessonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()
    viewing_time = serializers.IntegerField()


class SpecificProducSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    status = serializers.CharField()
    viewing_time = serializers.IntegerField()
    last_viewed = serializers.DateField()
