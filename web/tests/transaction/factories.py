import factory
from factory import fuzzy
from tests.wallet.factories import WalletFactory
from transaction.models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    comment = fuzzy.FuzzyText(length=64)
    wallet = factory.SubFactory(WalletFactory)
    balance = fuzzy.FuzzyDecimal(low=0.02, high=1000.00)
