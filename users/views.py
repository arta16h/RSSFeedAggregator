import jwt, datetime
import logging

from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import User
from.auth import JwtAuthentication
from .serializers import UserSerializer, LoginSerializer, LoginOTPSerializer, ChangePasswordSerializer

# Create your views here.

logger = logging.getLogger('django_API')

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"User {serializer.phone} created!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SendOTPAPIView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_otp(request, serializer.data["phone"])
            return Response (data={"message":"succeeded"})
        

class VerifyOTPAPIView(APIView):
    def post(self, request):
        serliazer=LoginOTPSerializer(data=request.data, context={"request":request})
        if serliazer.is_valid(raise_exception=True):
            user=User.objects.get(phone=request.session.get("phone"))
            access_token=user.get_access_token()
            refresh_token=user.get_refresh_token()
            return Response(data={"message":"succeeded", "AT":access_token, "RT":refresh_token})

        
class LoginAPIView(APIView):
    def post(self, request):
        password = request.data["password"]
        phone = request.data["phone"]
        user = User.objects.filter(phone= phone).first()

        if not User:
            raise APIException("User does not exist!")

        if not user.check_password(password):
            raise AuthenticationFailed("Password is not correct!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()}
        
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt":token}
        return response
    

class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "succeded"}
        return response
    

class ChangePasswordAPIView(APIView):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user:User = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not user.check_password(data["old_password"]):
            return Response({"detail": "invalid password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if user.check_password(data["new_password"]):
            return Response({"detail": "new password can not be same as old password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user.set_password(data["new_password"])
        user.save()
        return Response({"detail": "password changed successfully"}, status=status.HTTP_202_ACCEPTED)