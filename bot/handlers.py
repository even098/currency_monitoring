import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.services import register_user

router = Router()


class Register(StatesGroup):
    notify_time = State()


class Subscribe(StatesGroup):
    base_currency_code = State()
    target_currency_code = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Register.notify_time)
    await message.answer('Привет! Отправь время в 24-часовом формате HH:MM, '
                         'и начнешь получать уведомления в это время.')


@router.message(Register.notify_time)
async def set_notify_time(message: Message, state: FSMContext):
    await state.update_data(notify_time=message.text)
    data = await state.get_data()
    notify_time = data.get('notify_time')

    try:
        notify_time = datetime.strptime(notify_time, '%H:%M')
        await state.set_state(Subscribe.base_currency_code)
        await message.answer('А теперь отправьте код вашей базовой валюты (например, USD, EUR, KZT)')
        detail = await register_user(telegram_id=message.from_user.id, notify_time=notify_time.time())
        print(detail)
    except ValueError:
        await message.reply('❌ Некорректный формат! Введите в формате HH:MM (например, 09:30)')


@router.message(Subscribe.base_currency_code)
async def set_base_currency_code(message: Message, state: FSMContext):
    pass
