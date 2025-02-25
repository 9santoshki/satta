# betting/models.py

from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    betting_end_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']


class Outcome(models.Model):
    event = models.ForeignKey(
        Event, 
        related_name='outcomes', 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    total_bets = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.title} ({self.odds})"


class Bet(models.Model):
    user = models.ForeignKey(
        'accounts.UserProfile',  # Assuming you have a UserProfile model
        on_delete=models.CASCADE, 
        related_name="bets"
    )
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name="bets"
    )
    outcome = models.ForeignKey(
        Outcome, 
        on_delete=models.CASCADE, 
        related_name="bets"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_won = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    betting_end_time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Bet"
        verbose_name_plural = "Bets"

    def __str__(self):
        return f"Bet by {self.user.username if self.user else 'Unknown User'} on {self.event.title} for {self.amount}"
