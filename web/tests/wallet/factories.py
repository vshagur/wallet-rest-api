import factory
from factory import fuzzy
from wallet.models import Wallet


class WalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Wallet

    name = factory.Sequence(lambda n: "Wallet_%03d" % n)
    balance = fuzzy.FuzzyDecimal(0.01, 100.00, 2)
