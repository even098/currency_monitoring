from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .services import get_subscriptions


async def get_actions_markup():
    actions_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='My subscriptions'), KeyboardButton(text='Change notification time')],
            [KeyboardButton(text='New subscription')],
            [KeyboardButton(text='Delete subscription')]
        ],
        resize_keyboard=True,
    )

    return actions_markup


async def get_back_markup():
    back_markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Back')]
        ],
        resize_keyboard=True,
    )

    return back_markup


async def get_subscriptions_markup(telegram_id: int):
    subscriptions_markup = InlineKeyboardBuilder()
    subscriptions = await get_subscriptions(telegram_id)

    for subscription in subscriptions:
        subscriptions_markup.button(
            text=f'{subscription["base_currency_code"]} → {subscription["target_currency_code"]}',
            callback_data=f'delete:{subscription["base_currency_code"]}:{subscription["target_currency_code"]}'
        )

    return subscriptions_markup.adjust(1).as_markup()
