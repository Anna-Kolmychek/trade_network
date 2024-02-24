from rest_framework.exceptions import ValidationError

from traders.models import Trader


def get_trader_level(data):
    if data.get('vendor'):
        print('-'*50)
        print(data['vendor'])
        vendor = Trader.objects.get(pk=data['vendor'])
        if vendor.level == 3:
            raise ValidationError('Превышено количество звеньев в сети продаж (больше 3 уровней)')
        return vendor.level + 1
    return 0
