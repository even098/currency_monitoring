import socket
from datetime import datetime

import requests
from celery import shared_task

from backend.currency.models import Subscription

API_URL = f'http://127.0.0.1:8000/api'


@shared_task
def update_currency_rates():
    response = requests.get(f'{API_URL}/rates-update/').json()
    return response['detail']


@shared_task
def send_notifications():
    from .models import User
    from bot.main import send_message

    users = User.objects.filter(notify_time__hour=datetime.now().hour, notify_time__minute=datetime.now().minute)

    for user in users:
        message = ''
        for subscription in user.subscriptions.all():
            message += (f'1 {subscription.currency.base_currency_code} - {subscription.currency.rate} '
                        f'{subscription.currency.target_currency_code}\n')
            print(message)
        send_message(user.telegram_id, message)

    return 'notifications sent'
