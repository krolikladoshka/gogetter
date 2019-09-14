from django import urls
from rest_framework import routers

from exchange_watch import viewsets

exchanges_router = routers.DefaultRouter()

exchanges_router.register(r'^rate/(?p:[a-zA-Z]{3}-[a-zA-Z]$', viewset=viewsets.ExchangeRateViewset)

urlpatterns = []

urlpatterns += exchanges_router.urls
