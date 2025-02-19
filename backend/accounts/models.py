from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone

class UserProfile(AbstractUser):
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Increased max_digits for larger balances
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

    def deposit(self, amount: float):
        """Add a deposit to the user's balance."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.save()

    def withdraw(self, amount: float):
        """Withdraw funds from the user's balance."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.save()

    def get_balance(self):
        """Returns the current balance."""
        return self.balance

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
