from django.urls import path


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterAPIView,
    SendOTPView,
    LogoutAPIView,
    ProfileUpdateAPIView,
)
app_name = 'users'


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", RegisterAPIView.as_view(), name="register"),

    path("profile/update",ProfileUpdateAPIView.as_view(),name="profile-update"),
    path("logout/",LogoutAPIView.as_view(),name="logout"),
]