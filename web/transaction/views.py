from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response
from wallet.models import MINIMUM_ACCOUNT_BALANCE, Wallet

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionCreate(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaction.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('wallet__id',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        balance = Decimal(serializer.validated_data.get('balance'))
        wallet_id = request.data.get('wallet')
        wallet = get_object_or_404(Wallet, pk=wallet_id)
        new_balance = wallet.balance + balance

        if new_balance < MINIMUM_ACCOUNT_BALANCE:
            data = {'detail': 'Insufficient funds to complete the transaction.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        else:
            wallet.balance = new_balance
            wallet.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TransactionRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Transaction.objects.all()

    def destroy(self, request, *args, **kwargs):
        transaction_id = kwargs.get('pk')
        transaction = get_object_or_404(self.get_queryset(), pk=transaction_id)
        wallet = get_object_or_404(Wallet, pk=transaction.wallet.id)

        if wallet.balance - transaction.balance < MINIMUM_ACCOUNT_BALANCE:
            data = {'detail': 'It is not possible to delete a transaction.'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
