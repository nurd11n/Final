from django.contrib import admin
from .models import User, UserProfile, DriverProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(DriverProfile)
