from django.db import models
from django.contrib.auth import get_user_model
from .utils import cites_choices
from django.utils.text import slugify
from users.models import CustomUser
from django.urls import reverse
from PIL import Image
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_image(image):
    try:
        image = Image.open(image)
    except (IOError, ValueError):
        raise ValidationError("Invalid Image format")

    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image size must be less than 2MB")


class Attachment(models.Model):
    image = models.ImageField(
        blank=True,
        upload_to="attachments/",
        verbose_name="Images",
        validators=[validate_image],
        help_text="Allowed files are images with size less than or equal 2MB",
    )
    playground = models.ForeignKey(
        "Playground",
        related_name="images",
        on_delete=models.CASCADE,
    )


class Playground(models.Model):
    class Grass(models.TextChoices):
        ARTIFICIAL = "Artificial", "Artificial"
        NATURAL = "Natural", "Natural"

    CAPACITY_CHOICES = [(5, 5), (7, 7), (11, 11)]

    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES, default=5)
    # address = models.CharField(max_length=255)
    city = models.CharField(max_length=255, choices=cites_choices)
    grass_type = models.CharField(
        max_length=15, choices=Grass.choices, default=Grass.ARTIFICIAL
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playgrounds"
    )
    image = models.ImageField(upload_to="playgrounds_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("name", "city"),)
        ordering = ["name", "-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.owner.role == CustomUser.Role.PLAYER:
            raise PermissionError("only owners can add playgrounds")
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "core:playground_detail", kwargs={"pk": self.pk, "name": self.slug}
        )
