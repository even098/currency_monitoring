import os

import httpx
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()
API_URL = 'http://127.0.0.1:8000/api'
BASE_URL = os.getenv('BASE_URL')
API_KEY = os.getenv('API_KEY')


async def register_user(telegram_id: int, notify_time):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=f'{API_URL}/register/',
                timeout=10.0,
                data={'telegram_id': telegram_id, 'notify_time': notify_time}
            )
            response.raise_for_status()
            data = response.json()
            return data['detail']
        except httpx.HTTPStatusError as e:
            return f'HTTP Error: {e.response.status_code}'
        except Exception as e:
            return f'Error: {e}'


async def check_currency(currency_code: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=f'{API_URL}/currencies/',
                timeout=10.0,
            )
            response.raise_for_status()
            currencies = response.json()['supported_codes']

            for currency in currencies:  # currency here - is a list that contains currency code and name
                if currency_code in currency:
                    return True
            return False

        except httpx.HTTPStatusError as e:
            return f'HTTP error: {e.response.status_code}'
        except Exception as e:
            return f'Error: {e}'


async def subscribe_to_currency(telegram_id: int, base_currency_code: str, target_currency_code: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=f'{API_URL}/subscribe/',
                timeout=10.0,
                data={
                    'telegram_id': telegram_id,
                    'base_currency_code': base_currency_code,
                    'target_currency_code': target_currency_code
                }
            )
            response.raise_for_status()
            data = response.json()
            return data['detail']
        except httpx.HTTPStatusError as e:
            return f'HTTP Error: {e.response.status_code}'
        except Exception as e:
            return f'Error: {e}'


async def get_currency(base_currency_code: str, target_currency_code: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=f'{BASE_URL}/{API_KEY}/latest/{base_currency_code}',
                timeout=10.0,
            )
            data = response.json()
            response.raise_for_status()
            rate = data.get('conversion_rates').get(target_currency_code)
            return rate
        except Exception as e:
            return f'Error: {e}'


async def get_subscriptions(telegram_id: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=f'{API_URL}/subscriptions/',
                timeout=10.0,
                data={'telegram_id': f'{telegram_id}'}
            )
            data = response.json()
            response.raise_for_status()
            subscriptions = data.get('subscriptions', [])

            return subscriptions
        except Exception as e:
            return f'Error: {e}'


async def change_notification_time(telegram_id: int, notify_time):
    async with httpx.AsyncClient() as client:
        try:
            url = f'{API_URL}/change_notification_time/'
            response = await client.post(url=url, data={'telegram_id': telegram_id, 'notify_time': notify_time})
            response.raise_for_status()

            return response.json()['detail']
        except Exception as e:
            return f'Error: {e}'


async def delete_subscription(telegram_id: int, callback_data):
    async with httpx.AsyncClient() as client:
        try:
            url = f'{API_URL}/delete_subscription/'
            callback_data = callback_data.split(':')
            base_currency_code = callback_data[1]
            target_currency_code = callback_data[2]
            response = await client.post(
                url=url,
                data={
                    'telegram_id': telegram_id,
                    'base_currency_code': base_currency_code,
                    'target_currency_code': target_currency_code
                }
            )
            response.raise_for_status()

            return 'Deleted'
        except Exception as e:
            return f'Error: {e}'
