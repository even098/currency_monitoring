import httpx
from datetime import datetime


API_URL = 'http://localhost:8000/api'


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
            return f'Ошибка HTTP: {e.response.status_code}'
        except Exception as e:
            return f'Ошибка: {e}'


async def check_currency(telegram_id: int, currency_code: str):
    pass
