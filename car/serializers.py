from rest_framework import serializers
from .models import Category, Car


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    driver = serializers.ReadOnlyField(source='driver.name')
    class Meta:
        model = Car
        fields = '__all__'


# class SetCar(serializers.Serializer):
#     user = serializers.CharField(max_length=30)

