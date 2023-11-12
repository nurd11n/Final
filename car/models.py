from django.db import models
from account.models import DriverUser


class Category(models.Model):
    car_class = models.CharField(max_length=20, primary_key=True)


class Car(models.Model):
    driver = models.ForeignKey(DriverUser, related_name='car', blank=True, on_delete=models.SET_NULL, null=True)
    car_model = models.CharField(max_length=40)
    mileage = models.IntegerField()
    color = models.CharField(max_length=20)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='car')
    image = models.ImageField(blank=True, upload_to='car/')

    # def add_driver(self, new_driver):
    #     self.driver = new_driver
    #     return self.driver


