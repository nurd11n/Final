from rest_framework import serializers
from .models import Category, Car
from django.contrib.auth import get_user_model


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


# class SetCar(serializers.Serializer):
#     user = serializers.CharField(max_length=30)

