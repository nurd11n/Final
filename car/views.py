from .serializers import CarSerializer, CategorySerializer
from rest_framework import viewsets
from account.permissions import IsDriverProfile
from .models import Category, Car
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.permissions import AllowAny, IsAdminUser


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser, IsDriverProfile]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['car_model', 'color', 'category']
    search_fields = ['car_model', 'created_at', 'description']

    # @method_decorator(cache_page(60*5))
    # def retrieve(self, request, *args, **kwargs):
    #     return super().retrieve(request, *args, **kwargs)
    #
    # @method_decorator(cache_page(60*2))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

