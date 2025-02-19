from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Event, Outcome
from .serializers import EventSerializer, OutcomeSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ['status']

    def create(self, request, *args, **kwargs):
        """
        Custom create method for creating a new event.
        You can perform additional validation or processing here if needed.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Optionally handle outcomes creation or any other custom logic
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer
