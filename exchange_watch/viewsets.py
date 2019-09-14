from rest_framework import viewsets
from rest_framework.decorators import action

from exchange_watch.models import ExchangeRate
from exchange_watch.serializers import ExchangeRateDefaultSerializer


# NOTE: in real app we should probably restrict adding/deleting new exchanges for users w/o admin privileges
class ExchangeRateViewset(viewsets.mixins.ListModelMixin, viewsets.mixins.CreateModelMixin,
                          viewsets.mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateDefaultSerializer

    @action(url_path=r'[a-zA-Z]{3}-[a-zA-Z]{3}', url_name='retrieve-exchange', methods=['GET'], detail=False)
    def retrieve_rate(self, request, primary, secondary, *args, **kwargs):
        # TODO: resolve problems with action dispatching
        print(request)
        return self.list(*args, **kwargs)
