from django.db import models
from core.models import Playground
from django.core.validators import MinValueValidator
# Create your models here.
class Slot(models.Model):
    day = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    
    price = models.IntegerField(validators=[MinValueValidator(1)])
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)
    
    STATUS_CHOICES = [('free', 'FREE'), ('booked', 'BOOKED')]
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='FREE', help_text='Slot status')
    
    
    class Meta:
        unique_together = [('day', 'start_hour', 'end_hour', 'playground')]
    
    def __str__(self):
        return f"{self.day} : {self.start_hour} {self.end_hour}  {self.price}"
    