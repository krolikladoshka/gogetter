from typing import Any, Dict

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from exchange_watch import services
from exchange_watch.models import ExchangeRate
from exchange_watch.services import ExchangeRateService


# NOTE: should be marked as readonly serializer
class ExchangeRateDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = (
            'id',
            'primary',
            'secondary',
            'rate',
            'last_update_date_time',
        )


class CreateExchangeRateSerializer(serializers.ModelSerializer):

    def validate(self, data: Dict[str, Any]):
        service = ExchangeRateService()
        try:
            # NOTE: for now we just ignore all network exceptions, assuming that service is always available
            # NOTE: and we got perfect connection to net
            rate = service.get_exchange_rate(data['primary'], data['secondary'])
        except services.ExchangeRateNotFound:
            raise serializers.ValidationError('No such currency pair exists')

        data['rate'] = rate

        return data

    class Meta:
        model = ExchangeRate
        fields = (
            'primary',
            'secondary',
        )

        validators = (
            UniqueTogetherValidator(queryset=ExchangeRate.objects.all(), fields=('primary', 'secondary')),
        )
