from django.urls import path, include
from .views import OrderViewSet, OrderActivationAPIView, UserOrderHistoryAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('order/confirm/', OrderActivationAPIView.as_view()),
    path('order/history/', UserOrderHistoryAPIView.as_view()),
]