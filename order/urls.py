from django.urls import path, include
from .views import OrderViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]