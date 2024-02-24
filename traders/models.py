from django.db import models

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
    debt = models.DecimalField(max_digits=12, decimal_places=2, **NULLABLE, verbose_name='задолженность перед постащиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')

    def __str__(self):
        return self.title





