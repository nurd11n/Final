from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from car.models import Car
# from .models import DriverUser
# from .utils import send_activation_code
from .tasks import send_application_celery


DriverUser = get_user_model()


class DriverRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)
    class Meta:
        model = DriverUser
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'driver_license',
                  'is_car', 'car')

    # def set_car(self, validated_data):
    #     is_car = validated_data.pop('is_car', False)
    #     car_data = validated_data.pop('car_model', 'mileage', 'color', 'description', 'category', 'image', None)
    #     user = DriverUser.objects.create(**validated_data)
    #     if is_car and car_data:
    #         set_car = Car.objects.create(user=user, **car_data)
    #         user.car = set_car
    #         user.save()
    #     return user

    def create(self, validated_data):
        request = self.context.get('request')
        is_car = validated_data.pop('is_car', False)
        car_data = validated_data.pop('car', None)
        user = DriverUser.objects.create(**validated_data)
        if is_car and car_data:
            set_car = Car.objects.create(user=user, **car_data)
            user.drivers_car = set_car
            user.save()
        user = super().create(validated_data)
        user.create_activation_code()
        send_application_celery(
            request.user.first_name, request.user.last_name, request.user.driver_license,
            request.user.car, request.user.email, user.activation_code, request.user.name)
        return user

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise ValidationError('Passwords do not match!')
        return attrs

    def validate_email(self, email):
        if DriverUser.objects.filter(email=email).exists():
            return self.get_or_create(email=email)
            # raise serializers.ValidationError('User with this email already exist')
        return email


# class SetCarSerializer(serializers.ModelSerializer):
#
#     def set_car(self, driver, model, mileage, color, desc, category, image):
#         requests = self.context.get('request')
#         if requests.is_car:
#             requests.car = Car(
#                 driver=driver, model=model,
#                 mileage=mileage, color=color,
#                 description=desc, category=category,
#                 image=image
#             )
#         else:
#             pass
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         validated_data['car'] = request.user.car
#         instance = super().create(validated_data)
#         instance.set_car()
#         instance.create_activation_code()
#         send_application_celery(
#             request.user.first_name, request.user.last_name, request.user.driver_license,
#             request.user.car, request.user.email, instance.activation_code, request.user.name)
#         return instance


class GiveCarSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=10)

    def add_car(self, new_car):
        request = self.context.get('request')
        request.user.car = request.car
        return request

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['car'] = request.car
        instance = super().create(validated_data)
        instance.add_car()
        return instance

    def validate(self, attrs):
        password = attrs.get('password')
        if not password:
            raise serializers.ValidationError(
                'This password didn\'t match'
            )
        return attrs

