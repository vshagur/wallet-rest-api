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
