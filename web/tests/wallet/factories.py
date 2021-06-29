import factory
from wallet.models import MINIMUM_ACCOUNT_BALANCE, Wallet


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: "Wallet_%03d" % n)
    balance = MINIMUM_ACCOUNT_BALANCE
