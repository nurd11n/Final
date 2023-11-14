from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'price', 'car']

    def create(self, validated_data):
        super().create(validated_data)