# transactions/views.py
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.decorators import action

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        data = request.data
        transaction = Transaction.objects.create(
            user=data['user'],
            amount=data['amount'],
            transaction_type='deposit'
        )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        data = request.data
        transaction = Transaction.objects.create(
            user=data['user'],
            amount=data['amount'],
            transaction_type='withdrawal'
        )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def transaction_history(self, request, pk=None):
        transactions = Transaction.objects.filter(user_id=pk)
        return Response(TransactionSerializer(transactions, many=True).data)
