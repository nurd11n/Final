from django.db import models
from account.models import UserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.crypto import get_random_string
from car.models import Car
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _


class DriverUser(AbstractUser):
    username = None
    groups = models.ManyToManyField(Group, related_name='driver_user_accounts', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='driver_user_permissions', blank=True)
    email = models.EmailField(unique=True, primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    driver_license = models.CharField(default=None)
    is_car = models.BooleanField(default=False)
    car = models.ForeignKey(Car, related_name='driver_user', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='driver/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id} - {self.email}'

    def create_activation_code(self):
        code = get_random_string(length=15)
        self.activation_code = code

    def clean(self):
        if self.phone_number and not re.match(r'^\+?[0-9]+$', self.phone_number):
            self.add_error('phone_number', _('Please enter a valid phone number'))
            raise ValidationError(_('Invalid phone number format'))
        super().clean()



# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print(f'User {instance} was created {created}')
#     if created:
#         if instance.is_driver == True:
#             return DriverUser.objects.create(**instance)
#         else:
#             return User.objects.create(**instance)



