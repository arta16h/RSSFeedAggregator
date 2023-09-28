import jwt, datetime

from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.views import Response, APIView
from rest_framework import status

from .models import User
from .serializers import UserSerializer, LoginSerializer, LoginOTPSerializer

# Create your views here.

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class SendOTPAPIView(APIView):
    def post(self, request):
        serializer=LoginSerializer(data=request.data, context={"request":request})
        if serializer.is_valid(raise_exception=True):
            serializer.create_otp(request, serializer.data["phone"])
            return Response (data={"message":"200"})
        

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