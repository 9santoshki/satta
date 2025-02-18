from rest_framework import serializers
from .models import Event, Outcome

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['id', 'title', 'odds', 'created_at']

class EventSerializer(serializers.ModelSerializer):
    outcomes = OutcomeSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'status', 'created_at', 'updated_at', 'outcomes']
