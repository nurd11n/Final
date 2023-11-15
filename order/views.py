from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from account.permissions import IsDriverProfile
from .models import Order
from .serializers import OrderSerializer, OrderConfirmSerializer
from rest_framework.response import Response
from rest_framework import status


class OrderViewSet(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]


class OrderActivationAPIView(APIView):
    permission_classes = [IsDriverProfile]

    def post(self, request):
        serializer = OrderConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(in_stock=True)
        return Response('Order confirmed', status=status.HTTP_200_OK)


class UserOrderHistoryAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
