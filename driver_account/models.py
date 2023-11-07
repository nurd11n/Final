from django.db import models
from account.models import UserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from car.models import Car


class DriverUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=50)
    license = models.BooleanField(default=False)
    is_car = models.BooleanField(default=False)
    car = models.ForeignKey(Car, related_name='driver', blank=True)
    image = models.ImageField(blank=True, upload_to='driver/')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.id} - {self.email}'

    def create_activation_code(self):
        code = get_random_string(length=15)
        self.activation_code = code

    def add_car(self, new_car):
        self.car = new_car
        return self.car

