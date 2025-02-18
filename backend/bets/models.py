# bets/models.py
from django.db import models
from accounts.models import UserProfile
from events.models import Event, Outcome

class Bet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_won = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bet by {self.user.username} on {self.event.name} for {self.amount}"
