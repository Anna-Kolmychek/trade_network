from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from traders.models import Trader
from traders.serializers import TraderSerializer


class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']
