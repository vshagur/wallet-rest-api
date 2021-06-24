import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from tests.users.factories import UserFactory
from tests.wallet.factories import WalletFactory


@pytest.fixture()
def auth_client(test_user):
    client = APIClient()
    refresh = RefreshToken.for_user(test_user)
    client.force_authenticate(user=test_user, token=refresh.access_token)
    return client


@pytest.fixture()
def anon_client():
    client = APIClient()
    return client


@pytest.fixture()
def test_user():
    User = get_user_model()
    return User.objects.all().last()


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        WalletFactory.create_batch(10)
        UserFactory()
        yield
