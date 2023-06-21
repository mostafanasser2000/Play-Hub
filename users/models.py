from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUsermanager

# Create your models here.
class CustomeUser(AbstractUser, PermissionsMixin):
    username = None
    ROLE_CHOICES = [
        ("Player", "Player"),
        ("Owner", "Owner")
    ]
    email = models.EmailField('email address', unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="Onwer")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    
    objects = CustomUsermanager()
    
    def get_username(self) -> str:
        return self.email
    def __str__(self):
        return self.full_name
    
   