from django.db import models, IntegrityError
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string
from car.models import Car
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# class DriverUserManager(BaseUserManager):
#     def _create_driver_user(self, email, password, phone_number, last_name, first_name, driver_license, is_car, car, **extra_fields):
#         if not email:
#             raise ValueError('Email field is required!')
#         email = self.normalize_email(email)
#
#         # Check if the user already exists
#
#         existing_user = self.model.objects.filter(email=email).first()
#
#         if existing_user:
#             # Handle the situation where the user already exists
#             # You might want to update the existing user or raise an error
#             existing_user.phone_number = phone_number
#             existing_user.last_name = last_name
#             existing_user.first_name = first_name
#             existing_user.driver_license = driver_license
#             existing_user.is_car = is_car
#             existing_user.car = car
#             existing_user.create_activation_code()
#             existing_user.set_password(password)  # Update the password if needed
#             existing_user.save()
#             return existing_user
#         else:
#             # Proceed with creating a new user
#             try:
#                 user = self.model(
#                     email=email, password=make_password(password),
#                     phone_number=phone_number, last_name=last_name,
#                     first_name=first_name, driver_license=driver_license,
#                     is_car=is_car, car=car, **extra_fields
#                 )
#                 user.create_activation_code()
#                 user.save()
#                 return user
#             except IntegrityError:
#                 # Handle the IntegrityError, possibly log it or raise a custom exception
#                 raise IntegrityError("User creation failed due to IntegrityError.")
#
#     def create_user(self, email, password, phone_number, last_name, first_name, driver_license, is_car, car,
#                     **extra_fields):
#         user = self._create_driver_user(
#             email=email, password=password,
#             phone_number=phone_number, last_name=last_name,
#             first_name=first_name, driver_license=driver_license,
#             is_car=is_car, car=car, **extra_fields
#         )
#         return user

    #     user = self.model(
    #         email=email, password=password,
    #         phone_number=phone_number, last_name=last_name,
    #         first_name=first_name, driver_license=driver_license,
    #         is_car=is_car, car=car, **extra_fields
    #     )
    #     user.set_password(password)
    #     user.create_activation_code()
    #     user.save()
    #     return user
    #
    # def create_user(self, email, password, phone_number, last_name, first_name, driver_license, is_car, car, **extra_fields):
    #     user = self._create_user(
    #         email=email, password=password,
    #         phone_number=phone_number, last_name=last_name,
    #         first_name=first_name, driver_license=driver_license,
    #         is_car=is_car, car=car, **extra_fields
    #     )
    #     return user


class DriverUser(User):
    # username = None
    # groups = models.ManyToManyField(Group, related_name='driver_user_accounts', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='driver_user_permissions', blank=True)
    # email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    # is_active = models.BooleanField(default=False)
    # activation_code = models.CharField(max_length=10, blank=True)
    # first_name = models.CharField(max_length=40)
    # last_name = models.CharField(max_length=50)
    driver_license = models.CharField(max_length=20)
    is_car = models.BooleanField(default=False)
    # car = models.OneToOneField(Car, related_name='driver_user_car', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=True, upload_to='driver/')

    # objects = UserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id} - {self.email}'

    # def save(self, *args, **kwargs):
    #     if self.is_driver == True:
    #         return DriverUser.objects.create(*args, **kwargs)
    #     super().save(*args, **kwargs)

    # def create_activation_code(self):
    #     code = get_random_string(length=15)
    #     self.activation_code = code
    #
    # def clean(self):
    #     if self.phone_number and not re.match(r'^\+?[0-9]+$', self.phone_number):
    #         self.add_error('phone_number', _('Please enter a valid phone number'))
    #         raise ValidationError(_('Invalid phone number format'))
    #     super().clean()



# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print(f'User {instance} was created {created}')
#     if created:
#         if instance.is_driver == True:
#             return DriverUser.objects.create(**instance)
#         else:
#             return User.objects.create(**instance)



