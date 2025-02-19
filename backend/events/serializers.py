from rest_framework import serializers
from .models import Event, Outcome

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        fields = ['id', 'title', 'odds', 'event']

class EventSerializer(serializers.ModelSerializer):
    outcomes = OutcomeSerializer(many=True)  # Nested Outcome serializer

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 'status', 'outcomes']

    def create(self, validated_data):
        outcomes_data = validated_data.pop('outcomes', [])
        event = Event.objects.create(**validated_data)  # Create the event itself
        # Now create the outcomes associated with this event
        for outcome_data in outcomes_data:
            Outcome.objects.create(event=event, **outcome_data)
        return event
