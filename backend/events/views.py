from rest_framework import viewsets
from .models import Event, Outcome
from .serializers import EventSerializer, OutcomeSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ['status']

class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
