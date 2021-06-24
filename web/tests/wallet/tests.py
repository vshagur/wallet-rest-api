from decimal import Decimal

import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from wallet.models import Wallet


def test_anon_client_can_not_get_wallets_list(anon_client):
    resp = anon_client.get(reverse('wallet-list'))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_anon_client_can_not_get_wallet_detail(anon_client):
    resp = anon_client.get(reverse('wallet-list'))
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_anon_client_can_not_create_wallet(anon_client):
    count = Wallet.objects.all().count()
    resp = anon_client.post(reverse('wallet-list'), data={'name': 'bitcoin_wallet'})
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    assert Wallet.objects.all().count() == count


@pytest.mark.django_db
def test_auth_client_can_create_wallet(auth_client):
    count = Wallet.objects.all().count()
    resp = auth_client.post(reverse('wallet-list'), data={'name': 'bitcoin_wallet'})
    assert resp.status_code == status.HTTP_201_CREATED
    assert Wallet.objects.all().count() == count + 1
    resp_data = resp.json()
    assert 'id' in resp_data
    pk = resp_data.get('id')
    assert Wallet.objects.filter(id=pk).exists()
    wallet = Wallet.objects.get(id=pk)
    assert resp_data.get('name') == wallet.name
    assert Decimal(str(resp_data.get('balance'))) == wallet.balance


def test_auth_client_can_get_wallets_list(auth_client):
    resp = auth_client.get(reverse('wallet-list'))
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) == 10


@pytest.mark.django_db
def test_auth_client_can_get_wallet_detail(auth_client):
    wallet = Wallet.objects.all().last()
    resp = auth_client.get(reverse('wallet-detail', args=(wallet.id,)))
    assert resp.status_code == status.HTTP_200_OK
    resp_data = resp.json()
    assert resp_data.get('id') == wallet.id
    assert resp_data.get('name') == wallet.name
    assert Decimal(str(resp_data.get('balance'))) == wallet.balance
