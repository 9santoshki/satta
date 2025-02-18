# transactions/models.py
from django.db import models
from accounts.models import UserProfile

class Transaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.user.username}"
