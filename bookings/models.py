from django.db import models
from django.db.models.query import QuerySet
from slots.models import Slot
from django.contrib.auth import get_user_model

User = get_user_model()


class PendingManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status="pending")


class Booking(models.Model):
    class Status(models.TextChoices):
        ACCEPTED = "accepted", "accepted"
        REJECTED = "rejected", "rejected"
        PENDING = "pending", "pending"

    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    objects = models.Manager()
    pending = PendingManager() 
    class Meta:
        unique_together = [("slot", "player")]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"{self.player} booked {self.slot}"
