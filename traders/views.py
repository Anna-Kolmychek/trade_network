from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from traders.models import Trader
from traders.serializers import TraderSerializer
from traders.services import get_trader_level


class TraderViewSet(viewsets.ModelViewSet):
    queryset = Trader.objects.all()
    serializer_class = TraderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

    def create(self, request, *args, **kwargs):
        request.data['level'] = get_trader_level(request.data)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data['level'] = get_trader_level(request.data)
        return super().update(request, *args, **kwargs)
