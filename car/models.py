from django.db import models
from django.contrib.auth import get_user_model


DriverUser = get_user_model()


class Category(models.Model):
    place_class = models.CharField(max_length=20, primary_key=True)


class Car(models.Model):
    driver = models.ForeignKey(User, related_name='car', blank=True)
    model = models.CharField(max_length=40)
    mileage = models.IntegerField(max_length=20)
    color = models.CharField(max_length=20)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='car')
    image = models.ImageField(blank=True, upload_to='car/')

    def add_driver(self, new_driver):
        self.driver = new_driver
        return self.driver


