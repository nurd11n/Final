from rest_framework import serializers
from .models import Category, Car


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    # driver = serializers.ReadOnlyField(source='driver.name')

    class Meta:
        model = Car
        fields = '__all__'
