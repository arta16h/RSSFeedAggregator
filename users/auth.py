from django.contrib.auth.backends import BaseBackend
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication

from .models import User
from .utils import JwtHelper
from config.settings import SECRET_KEY


class UserAuthBackend(BaseBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        

class JwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header=request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            raise AuthenticationFailed
        
        print(auth_header)
        prefix,token=auth_header.split()
        if not prefix=='Bearer':
            raise AuthenticationFailed
        user_id=JwtHelper.validate_jwt_token(token,SECRET_KEY)
        if not user_id:
            raise AuthenticationFailed(_("User not Found!"))
        user=User.objects.get(id=user_id)
        return user,token