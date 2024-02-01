from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _


class CustomUsermanager(BaseUserManager):
    def create_user(self, email, password=None, role=None):
        """
        Create and saves a User with the given email and password and role
        """

        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), role=role)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves the superuser with the given email, password
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
