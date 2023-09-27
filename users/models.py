from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, phone, password, **other_fields):
        if not phone:
            raise ValueError("The Phone Field Can Not Be Empty!")

        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

