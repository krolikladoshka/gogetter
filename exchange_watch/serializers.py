from rest_framework import serializers

from exchange_watch.models import ExchangeRate


class ExchangeRateDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = (
            'primary',
            'secondary',
            'rate',
            'last_update_date_time',
        )
