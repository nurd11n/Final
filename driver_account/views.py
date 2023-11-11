from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import DriverUser
from .serializers import GiveCarSerializer, DriverRegistrationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class DriverRegistration(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = DriverRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Driver is registered', status=200)


class GiveCarViewSet(APIView):
    permission_classes = [IsAdminUser]
    def post(self, request):
        serializer = GiveCarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Car was given', status=200)


class ActivationDriverView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request, email, activation_code):
        try:
            user = DriverUser.objects.get(email=email, activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            return Response(
                {"Message": "Successfully activated."},
                status=status.HTTP_200_OK
            )
        except DriverUser.DoesNotExist:
            return Response(
                {"Message": "Wrong email."},
                status=status.HTTP_400_BAD_REQUEST
            )

