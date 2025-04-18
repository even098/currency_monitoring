# Generated by Django 5.1.6 on 2025-03-16 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0004_remove_currency_base_currency_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='base_currency_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='currency',
            name='target_currency_code',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='currency',
            unique_together={('base_currency_code', 'target_currency_code')},
        ),
    ]
