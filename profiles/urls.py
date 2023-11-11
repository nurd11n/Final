from django.urls import path
from .views import GiveCarViewSet, DriverRegistration


urlpatterns = [
    path('register-driver/', DriverRegistration.as_view()),
    path('give-car/', GiveCarViewSet.as_view()),
]