# bets/serializers.py
from rest_framework import serializers
from .models import Bet

class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bet
        fields = ('id', 'user', 'event', 'outcome', 'amount', 'is_won', 'created_at')
