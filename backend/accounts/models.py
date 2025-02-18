# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Add any additional fields if necessary, like address, phone number, etc.

    def __str__(self):
        return self.username
