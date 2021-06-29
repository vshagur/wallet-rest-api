from decimal import Decimal

import factory
from factory import fuzzy
from tests.wallet.factories import WalletFactory
from transaction.models import Transaction


class TransactionFactory(factory.django.DjangoModelFactory):
    comment = fuzzy.FuzzyText(length=64)
    balance = fuzzy.FuzzyDecimal(low=0.02, high=1000.00)
    wallet = factory.SubFactory(WalletFactory)

    class Meta:
        model = Transaction

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        wallet = kwargs.get('wallet')
        balance = kwargs.get('balance')

        if isinstance(balance, float):
            balance = str(balance)

        if isinstance(balance, str):
            balance = Decimal(balance)

        wallet.balance += balance
        wallet.save()
        obj.save()
        return obj
