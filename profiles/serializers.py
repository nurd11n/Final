from car.models import Car
from .models import DriverUserProfile
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
# from .utils import send_activation_code
# from .tasks import send_activation_code_celery


class DriverRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverUserProfile
        fields = 'email', 'first_name', 'last_name', 'driver_license', 'is_car', 'car'

    def set_car(self, **kwargs):
        if self.is_car == True:
            self.car = Car()
            return self.car
        self.car = False
        return self.car

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['car'] = request.car
        instance = super().create(validated_data)
        # instance.set_car()
        instance.create_activation_code()
        # send_order_email(request.user.email, instance.activation_code, request.user.name)
        return instance


class GiveCarSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=10)

    def validate_email(self, email):
        if DriverUserProfile.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exist')
        return email

    def add_car(self, new_car):
        self.car = new_car
        return self.car

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['car'] = request.car
        instance = super().create(validated_data)
        instance.add_car()
        # instance.create_activation_code()
        # send_order_email(request.user.email, instance.activation_code, request.user.name)
        return instance

    def validate(self, attrs):
        password = attrs.get('password')
        if not password:
            raise serializers.ValidationError(
                'This password didn\'t match'
            )
        return attrs


