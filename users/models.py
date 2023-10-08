import re

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from .utils import JwtHelper
from config import settings
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other_fields):
        if not phone:
            raise ValueError("The Phone Field Can Not Be Empty!")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **other_fields)
    
PHONE_REGEX_PATTERN = r"^(\\+98|0)?9\d{9}$"

def phone_validator(phone:str):
    if not (matched := re.fullmatch(PHONE_REGEX_PATTERN, phone.strip())):
        raise ValidationError("Invalid phone number!")
    return matched


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(validators=[phone_validator], unique=True, max_length=20)
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def get_access_token(self):
        return JwtHelper.generate_jwt_token(self.id, settings.SECRET_KEY, 30)
    
    def get_refresh_token(self):
        return JwtHelper.generate_jwt_token(self.id, settings.SECRET_KEY, 720)

    def __str__(self):
        return f"{self.phone}"