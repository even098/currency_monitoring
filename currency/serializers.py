from rest_framework import serializers

from .models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['base_currency_code', 'target_currency_code', 'rate', 'last_updated']
        read_only_fields = fields
