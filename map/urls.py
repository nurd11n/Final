from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('locations', LocationsView)

urlpatterns = [
    path("home/", HomeView.as_view(), name='my_home_view'),
    path("geocoding/<int:pk>/", GeocodingView.as_view(), name='my_geocoding_view'),
    path("distance/", DistanceView.as_view(), name='my_distance_view'),
    path("map/", MapView.as_view(), name='my_map_view'),
    path("", include(router.urls)),
]

# <iframe src="https://storage.googleapis.com/maps-solutions-eszug7ljox/address-selection/elbz/address-selection.html"
#   width="100%" height="100%"
#   style="border:0;"
#   loading="lazy">
# </iframe>


