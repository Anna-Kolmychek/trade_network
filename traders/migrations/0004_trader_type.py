# Generated by Django 5.0.2 on 2024-02-24 14:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trader_types', '0002_auto_20240224_1416'),
        ('traders', '0003_alter_trader_debt_alter_trader_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='trader',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trader_types.tradertypes', verbose_name='тип звена'),
        ),
    ]