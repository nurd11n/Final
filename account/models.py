from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
from django.db import models
from car.models import Car
import re
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required!')
        email = self.normalize_email(email)
        user = self.model(
            email=email, **extra_fields
        )
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, phone_number, first_name, last_name, **extra_fields):
        user = self._create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(
            email=email,
            password=password,
            phone_number='0507500888',
            first_name='admin',
            last_name='admin',
            **extra_fields
        )


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    is_driver = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id} - {self.email}'

    def create_activation_code(self):
        code = get_random_string(length=10)
        self.activation_code = code

    def clean(self):
        if self.user.phone_number and not re.match(r'^\+?[0-9]+$', self.user.phone_number):
            raise ValidationError(_('Invalid phone number format'))
        super().clean()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile', primary_key=True)
    driver_license = models.CharField(max_length=20, blank=False)
    is_car = models.BooleanField(default=False)
    car = models.OneToOneField(Car, related_name='driver_user_car', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='driver/')

    def __str__(self):
        return f'{self.user.email} - {self.driver_license} - {self.car}'

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, instance, created, **kwargs):
#     is_driver = getattr(instance, 'is_driver', False)
#     if created and not is_driver:
#         UserProfile.objects.create(user=instance)
#         print(f'User {instance} was created {created}')
#     else:
#         DriverProfile.objects.create(user=instance)
#         print(f'Driver {instance} was created {created}')
