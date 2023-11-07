from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarViewSet, CategoryViewSet


router = DefaultRouter()
router.register('car', CarViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
