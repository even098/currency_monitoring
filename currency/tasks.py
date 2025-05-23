import asyncio
import socket
from datetime import datetime

import requests
from aiogram import Bot
from celery import shared_task
from django.utils.timezone import now

from currency.models import Subscription, AvailableCurrency, User
from currency_monitoring.settings import BOT_TOKEN

API_URL = f'http://127.0.0.1:8000/api'
bot = Bot(token=BOT_TOKEN)


@shared_task
def update_currency_rates():
    response = requests.get(f'{API_URL}/rates_update/').json()
    return response['detail']


@shared_task
def send_notifications():
    task_message = 'nothing to sent'
    current_hour = now().hour
    current_minute = now().minute
    users = User.objects.filter(notify_time__hour=current_hour, notify_time__minute=current_minute)

    for user in users:
        subscriptions = user.subscriptions.all()
        if not subscriptions:
            continue

        message = '\n'.join([
            f"💱 <b>1 {s.currency.base_currency_code}</b> = <b>{s.currency.rate}</b> {s.currency.target_currency_code}"
            for s in subscriptions
        ])

        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        params = {
            'chat_id': user.telegram_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.get(url, params=params).json()
        task_message = 'sent message'

    return task_message


@shared_task
def update_available_currencies():
    response = requests.get(f'{API_URL}/currencies/').json()
    supported_codes = response['supported_codes']

    for supported_code in supported_codes:
        code, name = supported_code.split(',')
        AvailableCurrency.objects.get_or_create(code=code, name=name)

    return 'available currencies updated'
