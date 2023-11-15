from rest_framework.serializers import ModelSerializer
from .models import Locations, Distances


class LocationsSerializer(ModelSerializer):
    class Meta:
        model = Locations
        fields = '__all__'


class DistancesSerializer(ModelSerializer):
    class Meta:
        model = Distances
        fields = '__all__'