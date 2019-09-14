from django import urls
from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from exchange_watch import viewsets

exchanges_router = routers.DefaultRouter()
exchanges_router.register(r'rate', viewsets.ExchangeRateViewset)

urlpatterns = [
    path('', include(exchanges_router.urls)),
]
