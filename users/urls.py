from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, SendOTPAPIView, VerifyOTPAPIView

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="register"),
    path("login", LoginAPIView.as_view(), name="login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("sendotp/",SendOTPAPIView.as_view(), name="sendotp"),
    path("verify/", VerifyOTPAPIView.as_view(), name="verify"),
]