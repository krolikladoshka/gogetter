from rest_framework import viewsets

from exchange_watch.models import ExchangeRate
from exchange_watch.serializers import ExchangeRateDefaultSerializer, CreateExchangeRateSerializer
from exchange_watch.services import ExchangeRateService


# NOTE: in real app we should probably restrict adding/deleting new exchanges for users w/o admin privileges
class ExchangeRateViewset(viewsets.mixins.ListModelMixin, viewsets.mixins.RetrieveModelMixin,
                          viewsets.mixins.CreateModelMixin,
                          viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateDefaultSerializer
    service = ExchangeRateService()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateExchangeRateSerializer
        return self.serializer_class

    def get_first_rate_data(self, primary: str = None, secondary: str = None):
        return self.service.get_exchange_rate(primary, secondary)
