# bets/views.py
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Bet
from .serializers import BetSerializer
from rest_framework.decorators import action

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

    @action(detail=False, methods=['post'])
    def place_bet(self, request):
        data = request.data
        bet = Bet.objects.create(
            user=data['user'],
            event=data['event'],
            outcome=data['outcome'],
            amount=data['amount']
        )
        return Response(BetSerializer(bet).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def bet_history(self, request, pk=None):
        bets = Bet.objects.filter(user_id=pk)
        return Response(BetSerializer(bets, many=True).data)
