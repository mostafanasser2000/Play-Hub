from django.db import models
from django.db.models.query import QuerySet
from core.models import Playground
from django.core.validators import MinValueValidator
import datetime
from django.db.models import Q


class FreeManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .filter(Q(status="free") & Q(day__gte=datetime.date.today()))
        )


class BookedManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status="booked")


class Slot(models.Model):
    class Status(models.TextChoices):
        FREE = "free", "free"
        BOOKED = "booked", "booked"

    day = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    price = models.IntegerField(validators=[MinValueValidator(1)])
    playground = models.ForeignKey(
        Playground, on_delete=models.CASCADE, related_name="slots"
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.FREE,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    free_slots = FreeManager()
    booked_slots = BookedManager()

    class Meta:
        ordering = ["-created_at"]
        unique_together = [("day", "start_hour", "end_hour", "playground")]
        verbose_name = "Slot"
        verbose_name_plural = "Slots"

    def save(self, *args, **kwargs):
        if not self.status:
            self.status = self.Status.FREE
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.playground}-{self.day}-{self.start_hour}:{self.end_hour} Price:{self.price}"
