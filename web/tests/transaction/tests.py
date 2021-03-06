from decimal import Decimal

import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from transaction.models import Transaction
from wallet.models import Wallet

from .factories import TransactionFactory


def test_anon_client_can_not_get_transactions_list(anon_client):
    resp = anon_client.get(reverse('transaction-list'))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_anon_client_can_not_get_transaction_detail(anon_client):
    resp = anon_client.get(reverse('transaction-list'))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_auth_client_can_get_transaction_detail(auth_client):
    transaction = Transaction.objects.all().last()
    resp = auth_client.get(reverse('transaction-detail', args=(transaction.id,)))
    assert resp.status_code == status.HTTP_200_OK
    resp_data = resp.json()
    assert resp_data.get('id') == transaction.id
    assert resp_data.get('comment') == transaction.comment
    assert resp_data.get('wallet') == transaction.wallet.id
    assert Decimal(str(resp_data.get('balance'))) == transaction.balance


def test_auth_client_can_get_transactions_list(auth_client):
    count = Transaction.objects.all().count()
    resp = auth_client.get(reverse('transaction-list'))
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == count


@pytest.mark.django_db
class TestCreateTransaction:

    @classmethod
    def setup_class(cls):
        cls.wallet = Wallet.objects.first()
        cls.balance = cls.wallet.balance
        cls.transactions = Transaction.objects.all()
        cls.count = cls.transactions.count()
        cls.url = reverse('transaction-list')
        cls.data = {
            'wallet': cls.wallet.id,
            'comment': 'some comment',
            'balance': '42.42',
        }

    def test_anon_client_can_not_create_transaction(self, anon_client):
        balance = self.wallet.balance
        resp = anon_client.post(self.url, data=self.data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert Transaction.objects.all().count() == self.count
        assert Wallet.objects.get(pk=self.wallet.id).balance == balance

    @pytest.mark.django_db
    def test_auth_client_can_create_transaction(self, auth_client):
        resp = auth_client.post(self.url, data=self.data)
        assert resp.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.all().count() == self.count + 1
        resp_data = resp.json()
        assert 'id' in resp_data
        pk = resp_data.get('id')
        assert Transaction.objects.filter(id=pk).exists()
        assert resp_data.get('comment') == self.data.get('comment')
        assert resp_data.get('wallet') == self.wallet.id
        assert Decimal(str(resp_data.get('balance'))) == Decimal(self.data.get('balance'))
        transaction = Transaction.objects.get(id=pk)
        assert transaction.comment == self.data.get('comment')
        assert transaction.wallet == self.wallet
        assert transaction.balance == Decimal(self.data.get('balance'))
        updated_wallet = Wallet.objects.get(pk=self.wallet.id)
        assert updated_wallet.balance == self.balance + Decimal(self.data.get('balance'))

    @pytest.mark.django_db
    def test_auth_client_can_create_transaction_decrease_balance(self, auth_client):
        transaction = TransactionFactory(balance=Decimal('100.0'))
        count = Transaction.objects.all().count()
        balance = Decimal('-50.02')
        data = self.data.copy()
        data['wallet'] = transaction.wallet.id
        data['comment'] = 'comment: -50.02'
        data['balance'] = f'{balance}'
        expected_balance = transaction.wallet.balance + balance
        resp = auth_client.post(self.url, data=data)
        # check response
        assert resp.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.all().count() == count + 1
        resp_data = resp.json()
        assert 'id' in resp_data
        pk = resp_data.get('id')
        assert Transaction.objects.filter(id=pk).exists()
        assert resp_data.get('comment') == data.get('comment')
        assert resp_data.get('wallet') == transaction.wallet.id
        assert Decimal(str(resp_data.get('balance'))) == balance
        # check db
        transaction = Transaction.objects.get(id=pk)
        assert transaction.comment == data.get('comment')
        assert transaction.wallet == transaction.wallet
        assert transaction.balance == balance
        # check wallet balance
        updated_wallet = Wallet.objects.get(pk=transaction.wallet.id)
        assert updated_wallet.balance == expected_balance

    @pytest.mark.django_db
    def test_auth_client_can_not_create_transaction_if_balance_not_enough(
            self, auth_client):
        data = self.data.copy()
        balance_value = Wallet.objects.get(pk=self.wallet.id).balance + Decimal('0.01')
        data['balance'] = f'-{balance_value}'
        resp = auth_client.post(self.url, data=data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert Transaction.objects.all().count() == self.count


@pytest.mark.django_db
def test_auth_client_can_delete_transaction(auth_client):
    wallet = Wallet.objects.all().last()
    transaction = TransactionFactory(balance=Decimal('100.0'), wallet=wallet)
    transactions = Transaction.objects.all()
    count = transactions.count()
    resp = auth_client.delete(reverse('transaction-detail', args=(transaction.id,)))
    assert resp.status_code == status.HTTP_204_NO_CONTENT
    assert Transaction.objects.all().count() == count - 1
    assert not Transaction.objects.filter(pk=transaction.id).exists()
