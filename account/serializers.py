from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from driver_account.models import DriverUser
# from .utils import send_activation_code
from .tasks import send_activation_code_celery


User = get_user_model() # возвращает активную модельку юзера


class RegisterSerializer(ModelSerializer):
    password_confirm = CharField(min_length=5, required=True, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'phone_number', 'last_name', 'first_name']

    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        if pass1 != pass2:
            raise ValidationError('Passwords do not match!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        send_activation_code_celery.delay(user.email, user.activation_code)
        return user


# class RegisterDriverSerializer(serializers.ModelSerializer):
#     password_confirm = CharField(min_length=5, required=True, write_only=True)
#
#     class Meta:
#         model = DriverUser
#         fields = ['email', 'password', 'password_confirm', 'phone_number', 'last_name', 'first_name', 'is_driver']
#
#     def validate(self, attrs):
#         pass1 = attrs.get('password')
#         pass2 = attrs.pop('password_confirm')
#         if pass1 != pass2:
#             raise ValidationError('Passwords do not match!')
#         return attrs
#
#     def create(self, validated_data):
#         user = DriverUser.objects.create_user(**validated_data)
#         send_activation_code_celery.delay(user.email, user.activation_code)
#         return user


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


class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=5, write_only=True)










