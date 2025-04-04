# Generated by Django 5.1.6 on 2025-03-11 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0003_rename_base_code_currency_base_currency_code_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currency',
            name='base_currency_name',
        ),
        migrations.RemoveField(
            model_name='currency',
            name='target_currency_name',
        ),
        migrations.AlterField(
            model_name='currency',
            name='rate',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
