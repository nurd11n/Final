from django.db.models import Avg
from rest_framework import serializers
from account.models import User, UserProfile, DriverProfile
from account.tasks import send_activation_code_celery, send_application_celery
from review.serializers import CommentSerializer
from car.serializers import CarSerializer
from car.models import Car


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone_number', 'first_name', 'last_name', 'is_user', 'is_driver']


class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'last_name', 'first_name', 'phone_number']

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise serializers.ValidationError('Пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_user = True
        user.save()
        UserProfile.objects.create(user=user)
        user.create_activation_code()
        user.save()
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user


class DriverProfileSerializer(serializers.ModelSerializer):
    car = CarSerializer(required=False)

    class Meta:
        model = DriverProfile
        fields = ['driver_license', 'is_car', 'car', 'image']


class DriverSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=5, write_only=True)
    driver_profile = DriverProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            'email', 'password', 'password_confirm', 'last_name',
            'first_name', 'phone_number', 'driver_profile'
        ]

    def validate(self, attrs):
        password1 = attrs.get('password')
        password2 = attrs.pop('password_confirm')
        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def create(self, validated_data):
        driver_profile_data = validated_data.pop('driver_profile', None)
        user = User(**validated_data)
        user.is_driver = True
        user.set_password(validated_data['password'])
        user.create_activation_code()
        user.save()
        driver_profile_serializer = DriverProfileSerializer(data=driver_profile_data)
        if driver_profile_serializer.is_valid():
            driver_profile_serializer.save(user=user)
        else:
            raise serializers.ValidationError(driver_profile_serializer.errors)
        send_application_celery.delay(
            user.first_name, user.last_name,
            driver_profile_data['driver_license'], user.email, user.activation_code
        )
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        rep['likes'] = instance.likes.count()
        rep['favourites'] = instance.favourites.count()
        return rep


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
