from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UserProfile(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Add any additional fields if necessary, like address, phone number, etc.

    groups = models.ManyToManyField(
        Group,
        related_name="user_profiles",  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_profiles_permissions",  # Unique related_name
        blank=True
    )

    def __str__(self):
        return self.username
