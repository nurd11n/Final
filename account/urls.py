from rest_framework.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='activate'),
    path('change-password/', ChangePasswordView.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#driver_urls
    path('driver/register/', DriverRegistration.as_view()),
    path('driver/activate/<str:email>/<str:activation_code>/', ActivationDriverView.as_view(), name='activate-driver'),
    path('driver/give-car/', GiveCarViewSet.as_view()),
    path('driver/change-password/', ChangePasswordView.as_view()),
    path('driver/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('driver/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]