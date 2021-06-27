from decimal import Decimal

import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from transaction.models import Transaction
from wallet.models import Wallet


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


@pytest.mark.django_db
def test_anon_client_can_not_create_transaction(anon_client):
    wallet = Wallet.objects.first()
    count = Transaction.objects.all().count()
    data = {'wallet': wallet.id, 'comment': 'some comment', 'balance': '42.42', }
    resp = anon_client.post(reverse('transaction-list'), data=data)
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert Transaction.objects.all().count() == count


def test_auth_client_can_get_transactions_list(auth_client):
    resp = auth_client.get(reverse('transaction-list'))
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 10


@pytest.mark.django_db
class TestCreateTransaction:

    @classmethod
    def setup_class(cls):
        cls.wallet = Wallet.objects.first()
        cls.transactions = Transaction.objects.all()
        cls.count = cls.transactions.count()
        cls.url = reverse('transaction-list')
        cls.data = {
            'wallet': cls.wallet.id,
            'comment': 'some comment',
            'balance': '42.42',
        }

    def test_anon_client_can_not_create_transaction(self, anon_client):
        resp = anon_client.post(self.url, data=self.data)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED
        assert Transaction.objects.all().count() == self.count

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
