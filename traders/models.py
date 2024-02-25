from django.db import models
from rest_framework.exceptions import ValidationError

from products.models import Product
from trader_types.models import TraderTypes

NULLABLE = {'null': True, 'blank': True}


class Trader(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='название')
    type = models.ForeignKey(TraderTypes, on_delete=models.CASCADE, **NULLABLE, verbose_name='тип звена')
    level = models.PositiveIntegerField(verbose_name='уровень звена')
    email = models.EmailField(**NULLABLE, verbose_name='почта')
    country = models.CharField(max_length=100, **NULLABLE, verbose_name='страна')
    city = models.CharField(max_length=100, **NULLABLE, verbose_name='город')
    street = models.CharField(max_length=100, **NULLABLE, verbose_name='улица')
    house = models.CharField(max_length=10, **NULLABLE, verbose_name='№ дома')
    products = models.ManyToManyField(Product, **NULLABLE, verbose_name='продукты')
    vendor = models.ForeignKey('Trader', on_delete=models.CASCADE, **NULLABLE, verbose_name='поставщик')
    debt = models.DecimalField(max_digits=12, decimal_places=2, **NULLABLE,
                               verbose_name='задолженность перед постащиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    class Meta:
        ordering = ['pk']
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return self.title

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        check_vendor_eq_trader(self)
        self.level = get_trader_level(self.vendor)
        if not self._state.adding:
            check_level_for_children(self, self.level)
        super().save(force_insert, force_update, using, update_fields)
        if not self._state.adding:
            set_level_for_children(self, self.level)


def check_vendor_eq_trader(trader):
    if trader == trader.vendor:
        raise ValidationError('Поставщик продавца не может совпадать с самим продавцом')


def get_trader_level(vendor):
    if vendor:
        if vendor.level == 2:
            raise ValidationError('Превышено количество звеньев в сети продаж (больше 3 уровней)')
        return vendor.level + 1
    return 0


def check_level_for_children(trader, lvl):
    if trader:
        childern = Trader.objects.filter(vendor=trader).all()
        if childern and lvl == 2:
            raise ValidationError('Превышено количество звеньев в сети продаж (больше 3 уровней)')


def set_level_for_children(trader, lvl):
    if trader:
        childern = Trader.objects.filter(vendor=trader).all()

        for child in childern:
            child.level = lvl + 1
            set_level_for_children(child, lvl + 1)
            child.save()
