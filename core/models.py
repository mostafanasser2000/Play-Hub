from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Playground(models.Model):
    GRASS = [
        ('artificial','Artificial'),
        ('natural', 'Natural')
    ]
    CATCITY_CHOICES = [(5,5), (7,7), (11,11)]

    name = models.CharField(max_length=255)
    capcity = models.IntegerField(choices=CATCITY_CHOICES,default=5)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    grass_type = models.CharField(max_length=15, choices=GRASS, default='artificial')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media')
    
    class Meta:
        unique_together = (('name', 'address', 'city'),)
    
    def __str__(self) -> str:
        return self.name

        