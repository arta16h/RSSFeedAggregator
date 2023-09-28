from rest_framework import serializers

from .models import User

import random
from datetime import timedelta
from django.utils import timezone


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password",
        ]

    def create(self, validate_data):
        password = validate_data.pop("password", None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        else:
            raise ("Password field can not be empty!" )
        instance.save()
        return instance
    

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, allow_null=False)

    def validate(self, data):
        phone = data.get("phone")
        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError
        return data

    @staticmethod
    def create_otp(request, phone):
        request.session["otp"] = random.randint(1000, 9999)
        request.session["otp_expire"] = (timezone.now() + timedelta(minutes=10)).strftime("%d/%m/%Y, %H:%M:%S")
        request.session["phone"]=phone
        print(f"otp:{request.session['otp']}  until:{request.session['otp_expire']}")