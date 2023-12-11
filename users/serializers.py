from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import User

import random
from datetime import timedelta


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
            raise (_("Password field can not be empty!" ))
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


class LoginOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True, allow_null=False)

    def validate(self, data):
        otp = data.get("otp")
        request = self.context.get("request")
        if not otp == request.session.get("otp"):
            raise serializers.ValidationError
        if not User.objects.filter(phone=request.session.get("phone")).exists():
            raise serializers.ValidationError
        return data
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators = (validate_password,))
    confirm_password = serializers.CharField()

    def validate_digits(self, value):
        if 20<len(value)<6:
            raise ValidationError(_("Password must have between 6 to 20 digits"))
        return value

    def validate_confirm(self, data):
        if data['new_password'] != data['confirm_password']:
            print(data["new_password"], data["confirm_password"])
            raise serializers.ValidationError(_("Passwords don't match"))
        return data