from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_balance(self, value):

        if value == 0:
            raise serializers.ValidationError('balance is 0')

        return value

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'comment': instance.comment,
            'balance': instance.balance,
            'wallet': instance.wallet.id,
            'datetime': instance.datetime,
        }
