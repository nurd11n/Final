from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (DriverSignUpView, UserSignUpView, DriverOnlyView,
                    UserOnlyView, ChangePasswordView, ActivationView)


urlpatterns = [
    path('driver/signup/', DriverSignUpView.as_view()),
    path('user/signup/', UserSignUpView.as_view()),
    path('driver/dashboard', DriverOnlyView.as_view()),
    path('user/dashboard', UserOnlyView.as_view()),
    path('driver/change-password/', ChangePasswordView.as_view()),
    path('user/change-password/', ChangePasswordView.as_view()),
    path('driver/activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='driver-activate'),
    path('user/activate/<str:email>/<str:activation_code>/', ActivationView.as_view(), name='user-activate'),
    path('driver/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('driver/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]