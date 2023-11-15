from django.db import models
from django.contrib.auth import get_user_model
from car.models import Car

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='orders')
    CAR_CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('Comfort', 'Comfort')
    ]
    car_class = models.CharField(max_length=10, choices=CAR_CLASS_CHOICES)
    PAYMENT_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash')
    ]
    payment = models.CharField(max_length=4, choices=PAYMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.pk} by {self.user.email}"