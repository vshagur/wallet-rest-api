from django.db import models
from wallet.models import Wallet


class Transaction(models.Model):
    comment = models.TextField(
        null=False,
        blank=True,
        max_length=1024,
    )

    balance = models.DecimalField(
        null=False,
        max_digits=12,
        decimal_places=2,
    )

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
    )

    datetime = models.DateTimeField(
        auto_now_add=True,
        auto_created=True,
    )
