import sys

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.reverse import reverse

from .factories import WalletFactory
from wallet.models import Wallet


def test_example(db):
    obj = WalletFactory.create_batch(10)
    client = APIClient()
    resp = client.get(reverse('wallet-list'))
    assert resp.status_code == status.HTTP_200_OK

def test_example1(db):
    obj = WalletFactory.create_batch(10)
    wallet = Wallet.objects.all().first()
    client = APIClient()
    resp = client.get(reverse('wallet-detail',args=(wallet.id,)))
    assert resp.status_code == status.HTTP_200_OK
