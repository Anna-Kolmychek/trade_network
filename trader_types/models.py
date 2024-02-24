from django.db import models


class TraderTypes(models.Model):
    title = models.CharField(max_length=100, verbose_name='тип звена')

    def __str__(self):
        return self.title
