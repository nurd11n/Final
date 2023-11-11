from .permissions import IsProfileOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import GiveCarSerializer, DriverRegistrationSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


User = get_user_model()


class DriverRegistration(APIView):

    def post(self, request):
        serializer = DriverRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Driver is registered', status=200)


class GiveCarViewSet(APIView):
    permission_classes = [IsProfileOwner]

    def post(self, request):
        serializer = GiveCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Car was given', status=200)
