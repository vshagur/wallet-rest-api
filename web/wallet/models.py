from decimal import Decimal

from django.db import models

MINIMUM_ACCOUNT_BALANCE = Decimal('0.01')


class Wallet(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        max_length=256,
        unique=True,
    )

    balance = models.DecimalField(
        null=False,
        default=MINIMUM_ACCOUNT_BALANCE,
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return str(self.pk)
