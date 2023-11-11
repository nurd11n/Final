from rest_framework import serializers
from car.models import Car
from .models import DriverUser
# from .utils import send_activation_code
from .tasks import send_application_celery


class DriverRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverUser
        fields = 'email', 'first_name', 'last_name', 'driver_license', 'is_car'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['car'] = request.user.car
        instance = super().create(validated_data)
        instance.set_car()
        instance.create_activation_code()
        send_application_celery(
            request.user.first_name, request.user.last_name, request.user.driver_license,
            request.user.car, request.user.email, instance.activation_code, request.user.name)
        return instance


class SetCarSerializer(serializers.ModelSerializer):

    def set_car(self, driver, model, mileage, color, desc, category, image):
        requests = self.context.get('request')
        if requests.is_car:
            requests.car = Car(
                driver=driver, model=model,
                mileage=mileage, color=color,
                description=desc, category=category,
                image=image
            )
        else:
            pass

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['car'] = request.user.car
        instance = super().create(validated_data)
        instance.set_car()
        instance.create_activation_code()
        send_application_celery(
            request.user.first_name, request.user.last_name, request.user.driver_license,
            request.user.car, request.user.email, instance.activation_code, request.user.name)
        return instance


class GiveCarSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=10)

    def validate_email(self, email):
        if DriverUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exist')
        return email

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

