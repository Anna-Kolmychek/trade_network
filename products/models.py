from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название')
    model = models.CharField(max_length=100, default=None, **NULLABLE, verbose_name='Модель')
    release_date = models.DateField(default=None, **NULLABLE, verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f'{self.title} ({self.model})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
