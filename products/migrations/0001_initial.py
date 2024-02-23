# Generated by Django 5.0.2 on 2024-02-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Название')),
                ('model', models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Модель')),
                ('release_date', models.DateField(blank=True, default=None, null=True, verbose_name='Дата выхода продукта на рынок')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
    ]
