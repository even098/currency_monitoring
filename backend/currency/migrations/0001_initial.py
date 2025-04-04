# Generated by Django 5.1.6 on 2025-03-11 17:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_currency_code', models.CharField(max_length=10, unique=True)),
                ('target_currency_code', models.CharField(max_length=10, unique=True)),
                ('base_currency', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('target_currency', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.BigIntegerField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_time', models.TimeField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='currency.currency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='currency.user')),
            ],
            options={
                'unique_together': {('user', 'currency')},
            },
        ),
    ]
