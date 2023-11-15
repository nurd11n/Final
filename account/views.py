from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from review.models import Rating
from .permissions import IsUserProfile, IsDriverProfile
from .serializers import (UserSignUpSerializer, UserSerializer, DriverSignUpSerializer,
                          ChangePasswordSerializer)

User = get_user_model()


class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSignUpSerializer(user, context=self.get_serializer_context()).data,
            'message': "Account successfully registered"
        })


class DriverSignUpView(generics.GenericAPIView):
    serializer_class = DriverSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': DriverSignUpSerializer(user, context=self.get_serializer_context()).data,
            'message': "Account successfully registered"
        })


class ActivationView(APIView):
    def get(self, request, email, activation_code):
        try:
            user = User.objects.filter(email=email, activation_code=activation_code)
            user.is_active = True
            user.activation_code = ""
            user.save()
            return Response(
                {"Message": "Successfully activated."},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"Message": "Wrong email."},
                status=status.HTTP_400_BAD_REQUEST
            )


# class LogoutView(APIView):
#     def post(self, request, format=None):
#         request.auth.delete()
#         return Response(status=status.HTTP_200_OK)


class UserOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsUserProfile, IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class DriverOnlyView(generics.RetrieveAPIView):
    permission_classes = [IsDriverProfile, IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response('Password changed successfully', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RecommendationView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#
#         latest_ratings = Rating.objects.filter(user=user).order_by('-created_at')[:5]
#         if len(latest_ratings) < 10:
#             latest_ratings = Rating.objects.filter(user=user)
#
#         tags = []
#         for rating in latest_ratings:
#             film = rating.film
#             tags += film.tags.all()
#
#         return Response(.data)



