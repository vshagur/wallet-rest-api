from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('name', )

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'balance': instance.balance
        }
