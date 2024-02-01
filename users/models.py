from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUsermanager
from django.core.validators import RegexValidator


class CustomUser(AbstractBaseUser):
    class Role(models.TextChoices):
        PLAYER = "Player", "Player"
        OWNER = "Owner", "Owner"

    username = None
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\d{1,15}$",
                message="Phone number is Up to 15 digits allowed.",
            )
        ],
    )
    role = models.CharField(max_length=10, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  # user is superuser or not
    objects = CustomUsermanager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = (
        []
    )  # fields that is required when creating superuser, email, password are required by default

    objects = CustomUsermanager()

    def __str__(self):
        return self.email

    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        "Does the user has a specific permission"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label' ?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff"
        return self.is_admin
