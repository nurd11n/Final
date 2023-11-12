from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from car.models import Car


User = get_user_model()


class DriverUserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, primary_key=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    driver_license = models.CharField(default=None)
    is_car = models.BooleanField(default=False)
    car = models.ForeignKey(Car, related_name='driver_user', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='driver/')

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.car}'
#
#
# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     print(f'User {instance} was created {created}')
#     if created:
#         if instance.is_driver == True:
#             DriverUserProfile.objects.create(user=instance)
#         else:
#             UserProfile.objects.create(user=instance)


