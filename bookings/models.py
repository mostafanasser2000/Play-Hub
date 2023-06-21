from django.db import models
from slots.models import Slot
from users.models import CustomeUser


class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    player = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    BOOKING_STATUS = [
        ('accepted', 'accepted'),
        ('rejected','rejected'),
        ('pending', 'pending'),
    ]
    status = models.CharField(max_length=10, choices=BOOKING_STATUS, default='pending')
    
    def __str__(self):
        return f'{self.player} {self.slot}'

