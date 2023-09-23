from rest_framework import serializers


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    total_views = serializers.IntegerField()
    total_view_time = serializers.FloatField()
    total_students = serializers.IntegerField()
    purchase_percentage = serializers.FloatField()
