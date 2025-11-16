from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractBaseUser):
    phone_number = PhoneNumberField(unique=True, region='EG') 
    full_name = models.CharField(max_length=50)
    about = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='profiles/', blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.phone_number)
