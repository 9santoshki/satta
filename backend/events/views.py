from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Event, Outcome, Bet
from .serializers import EventSerializer, OutcomeSerializer, BetSerializer
from datetime import timezone

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    # Optionally, you can add a custom action here to handle event-specific logic, like closing the betting window:
    @action(detail=True, methods=['post'])
    def close_betting(self, request, pk=None):
        event = self.get_object()
        event.betting_end_time = timezone.now()
        event.save()
        return Response(EventSerializer(event).data, status=status.HTTP_200_OK)


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcome.objects.all()
    serializer_class = OutcomeSerializer

    @action(detail=True, methods=['post'])
    def add_outcome(self, request, pk=None):
        event = self.get_object()
        outcome = Outcome.objects.create(
            event=event,
            title=request.data.get('title'),
            odds=request.data.get('odds'),
        )
        return Response(OutcomeSerializer(outcome).data, status=status.HTTP_201_CREATED)


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

    # Custom action for placing a bet
    @action(detail=False, methods=['post'])
    def place_bet(self, request):
        data = request.data

        # Check if the event is open for betting (e.g., betting_end_time is not passed)
        event = Event.objects.get(id=data['event'])
        if event.betting_end_time <= timezone.now():
            return Response(
                {"detail": "Betting is closed for this event."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the bet
        bet = Bet.objects.create(
            user=data['user'],
            event=event,
            outcome=Outcome.objects.get(id=data['outcome']),
            amount=data['amount']
        )
        return Response(BetSerializer(bet).data, status=status.HTTP_201_CREATED)

    # Custom action to get bet history for a user
    @action(detail=True, methods=['get'])
    def bet_history(self, request, pk=None):
        bets = Bet.objects.filter(user_id=pk)
        return Response(BetSerializer(bets, many=True).data)
