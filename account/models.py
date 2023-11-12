from django.db import models
from django.contrib.auth.models import AbstractUser
from car.models import Car
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
import re
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email field is required!')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        user = self._create_user(email=email, password=password, **extra_fields)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    # phone_number = models.CharField(max_length=15)
    is_driver = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    # image = models.ImageField(blank=True, upload_to='driver/')
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
        if self.phone_number and not re.match(r'^\+?[0-9]+$', self.phone_number):
            self.add_error('phone_number', _('Please enter a valid phone number'))
            raise ValidationError(_('Invalid phone number format'))
        super().clean()


class DriverUser(User):
    phone_number = models.CharField(max_length=15, unique=True)
    driver_license = models.CharField(max_length=20)
    is_car = models.BooleanField(default=False)
    car = models.OneToOneField(Car, related_name='driver_user_car', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='driver/')

    def __str__(self):
        return f'{self.id} - {self.email} - {self.car}'

    # def save(self, *args, **kwargs):
    #     if self.is_driver == True:
    #         return DriverUser.objects.create(*args, **kwargs)
    #     super().save(*args, **kwargs)

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print(f'User {instance} was created {created}')
#     if instance.is_driver:
#         return DriverUserProfile.objects.create(user=instance)
#     else:
#         return User.objects.create(user=instance)
