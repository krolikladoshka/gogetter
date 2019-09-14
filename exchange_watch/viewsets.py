from rest_framework.viewsets import GenericViewSet
from exchange_watch.models import ExchangeRate
from exchange_watch.serializers import ExchangeRateDefaultSerializer


# NOTE: in real app we should probably restrict adding/deleting new exchanges for users w/o admin privileges
class ExchangeRateViewset(GenericViewSet):
    serializer_class = ExchangeRateDefaultSerializer

