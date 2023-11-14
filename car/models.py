from django.db import models


class Category(models.Model):
    car_class = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('Comfort', 'Comfort')
    ]
    car_class = models.CharField(max_length=10, primary_key=True, choices=car_class)


class Car(models.Model):
    # driver = models.OneToOneField(DriverProfile, on_delete=models.SET_NULL, related_name='car', null=True)
    car_model = models.CharField(max_length=255)
    mileage = models.IntegerField()
    color = models.CharField(max_length=20)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='car')
    image = models.ImageField(blank=True, upload_to='car/')

    def __str__(self):
        return self.car_model



