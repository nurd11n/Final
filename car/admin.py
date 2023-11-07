from django.contrib import admin
from .models import Category, Car


admin.register(Car, Category)
