from .serializers import CarSerializer, CategorySerializer
from rest_framework import viewsets
from .models import Category, Car
from rest_framework.permissions import IsAuthenticated, AllowAny


class MyPermissionMixin:
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class CategoryViewSet(MyPermissionMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CarViewSet(MyPermissionMixin, viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


