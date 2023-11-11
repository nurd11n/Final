from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from account.views import ChangePasswordView
from .views import GiveCarViewSet, DriverRegistration, ActivationDriverView


urlpatterns = [
    path('register/', DriverRegistration.as_view()),
    path('activate/<str:email>/<str:activation_code>/',ActivationDriverView.as_view(), name='activate-driver'),
    path('give-car/', GiveCarViewSet.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]