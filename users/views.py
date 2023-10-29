import jwt, datetime
from config.publisher_ import Publisher
import logging

from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import User
from.auth import JwtAuthentication
from .serializers import UserSerializer, LoginSerializer, LoginOTPSerializer, ChangePasswordSerializer

# Create your views here.

publisher = Publisher()

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publisher.publish(f"User {serializer.phone} created!", queue="signup-login")
        # logger.info(f"User {serializer.phone} created!")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SendOTPAPIView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_otp(request, serializer.data["phone"])
            publisher.publish("Serializer is valid! OTP was sent", queue="signup-login")
            # logger.info("Serializer is valid! OTP was sent")
            return Response (data={"message":"succeeded"})
        publisher.error_publish("Login serializer is Invalid!", queue="signup-login")
        # logger.error("Login serializer is Invalid!")
        return Response(status=status.HTTP_400_BAD_REQUEST)
        

class VerifyOTPAPIView(APIView):
    def post(self, request):
        serliazer=LoginOTPSerializer(data=request.data, context={"request":request})
        if serliazer.is_valid(raise_exception=True):
            user=User.objects.get(phone=request.session.get("phone"))
            access_token=user.get_access_token()
            refresh_token=user.get_refresh_token()
            # logger.info("otp verified!")
            return Response(data={"message":"succeeded", "AT":access_token, "RT":refresh_token})
        # logger.error("Login OTP Serializer is Invalid!")
        return Response(status=status.HTTP_400_BAD_REQUEST)

        
class LoginAPIView(APIView):
    def post(self, request):
        password = request.data["password"]
        phone = request.data["phone"]
        user = User.objects.filter(phone= phone).first()

        if not User:
            # logger.error("User does not exist!")
            raise APIException("User does not exist!")

        if not user.check_password(password):
            # logger.error("Password is not correct!")
            raise AuthenticationFailed("Password is not correct!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            "iat": datetime.datetime.utcnow()}
        
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {"jwt":token}
        # logger.info(f"User {phone} is now login!")
        return response
    

class LogoutAPIView(APIView):
    def post(self, _):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {"message": "succeded"}
        # logger.info("User got logout!")
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
            # logger.error("Invalid password!")
            return Response({"detail": "invalid password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        if user.check_password(data["new_password"]):
            return Response({"detail": "new password can not be same as old password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        user.set_password(data["new_password"])
        user.save()
        # logger.info(f"{user}'s password changed!")
        return Response({"detail": "password changed successfully"}, status=status.HTTP_202_ACCEPTED)