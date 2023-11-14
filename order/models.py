from django.db import models
from django.contrib.auth import get_user_model
from car.models import Car


User = get_user_model()


class Order(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    car_class = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('Comfort', 'Comfort')
    ]
    status = models.CharField(max_length=10, choices=car_class)
    payments = [
        ('Card', 'Card'),
        ('Cash', 'Cash')
    ]
    payment = models.CharField(max_length=4, choices=payments)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'order: {self.car}'
