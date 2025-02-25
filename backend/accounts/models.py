from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UserProfile(AbstractUser):
    # Balance field for users
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)  # Larger balance support

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
        return f"UserProfile: {self.username} (Balance: {self.balance})"

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

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['username']  # Default ordering by username
