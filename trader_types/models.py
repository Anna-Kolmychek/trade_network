from django.db import models


class TraderTypes(models.Model):
    title = models.CharField(max_length=100, verbose_name='тип звена')

    class Meta:
        ordering = ['id']
        verbose_name = 'Тип звена'
        verbose_name_plural = 'Типы звена'

    def __str__(self):
        return self.title
