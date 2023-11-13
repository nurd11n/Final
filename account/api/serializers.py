from rest_framework import serializers
from account.models import User, UserProfile, DriverProfile
from .tasks import send_activation_code_celery, send_application_celery
from car.models import Car


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'is_user']


class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'last_name', 'first_name', 'phone_number']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.is_user = True
        user.save()
        UserProfile.objects.create(user=user)
        return user

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password = serializers.CharField(required=True, min_length=5, write_only=True)
    new_password_confirm = serializers.CharField(required=True, min_length=5, write_only=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно')
        return old_password

    def validate(self, attrs):
        p1 = attrs['new_password']
        p2 = attrs['new_password_confirm']
        if p1 != p2:
            raise serializers.ValidationError('Пароли не совпадают')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        user.set_password(validated_data['new_password'])
        user.save(update_fields=['password'])
        return user


class DriverSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'last_name', 'first_name', 'phone_number', 'license', 'is_car', 'car'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def save(self, **kwargs):
        user = User(
            email=self.validated_data['email'],
        )
        user.set_password(self.validated_data['password'])
        user.is_driver = True
        user.save()
        DriverProfile.objects.create(user=user)
        return user

    def create(self, validated_data):
        request = self.context.get('request')
        is_car = validated_data.pop('is_car', False)
        car_data = validated_data.pop('car', None)
        user = DriverProfile.objects.create(**validated_data)
        if is_car and car_data:
            set_car = Car.objects.create(driver=user, **car_data)
            user.drivers_car = set_car
            user.save()
        user = super().create(validated_data)
        user.create_activation_code()
        send_application_celery(
            request.user.first_name, request.user.last_name, request.user.driver_license,
            request.user.car, request.user.email, user.activation_code, request.user.name)
        return user


# class DriverRegistrationSerializer(serializers.ModelSerializer):
#     password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)
#
#     class Meta:
#         model = DriverProfile
#         fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name', 'driver_license',
#                   'is_car', 'car')
#
#     # def set_car(self, validated_data):
#     #     is_car = validated_data.pop('is_car', False)
#     #     car_data = validated_data.pop('car_model', 'mileage', 'color', 'description', 'category', 'image', None)
#     #     user = DriverUser.objects.create(**validated_data)
#     #     if is_car and car_data:
#     #         set_car = Car.objects.create(user=user, **car_data)
#     #         user.car = set_car
#     #         user.save()
#     #     return user
#
#     def create(self, validated_data):
#         request = self.context.get('request')
#         is_car = validated_data.pop('is_car', False)
#         car_data = validated_data.pop('car', None)
#         user = DriverProfile.objects.create(**validated_data)
#         if is_car and car_data:
#             set_car = Car.objects.create(user=user, **car_data)
#             user.drivers_car = set_car
#             user.save()
#         user = super().create(validated_data)
#         user.create_activation_code()
#         send_application_celery(
#             request.user.first_name, request.user.last_name, request.user.driver_license,
#             request.user.car, request.user.email, user.activation_code, request.user.name)
#         return user
#
#     def validate(self, attrs):
#         pass1 = attrs.get('password')
#         pass2 = attrs.pop('password_confirm')
#         if pass1 != pass2:
#             raise ValidationError('Passwords do not match!')
#         return attrs
#
#     def validate_email(self, email):
#         if DriverProfile.objects.filter(email=email).exists():
#             return self.get_or_create(email=email)
#             # raise serializers.ValidationError('User with this email already exist')
#         return email
#
#
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
