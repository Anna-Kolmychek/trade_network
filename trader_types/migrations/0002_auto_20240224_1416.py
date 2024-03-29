# Generated by Django 5.0.2 on 2024-02-24 14:16

from django.db import migrations

from trader_types.models import TraderTypes


def create_trader_types(apps, schema_editor):
    trader_types = ['Завод', 'Розничная сеть', 'Индивидуальный предприниматель']

    for trade_type in trader_types:
        t = TraderTypes(title=trade_type)
        t.save()


class Migration(migrations.Migration):
    dependencies = [
        ('trader_types', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_trader_types),
    ]
