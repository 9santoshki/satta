from django.db import models
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_choices = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='upcoming')
    betting_end_time = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_time']

class Outcome(models.Model):
    event = models.ForeignKey(Event, related_name='outcomes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    odds = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    total_bets = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.title} ({self.odds})"
