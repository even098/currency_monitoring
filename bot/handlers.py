import re
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from .keyboard import get_actions_markup, get_back_markup, get_subscriptions_markup
from .services import register_user, check_currency, subscribe_to_currency, get_currency, get_subscriptions, \
    change_notification_time, delete_subscription

router = Router()
ERROR_MESSAGE = '⚠️ Something went wrong. Please try again later.'


class Register(StatesGroup):
    notify_time = State()


class Subscribe(StatesGroup):
    base_currency_code = State()
    target_currency_code = State()


class Change(StatesGroup):
    notify_time = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Register.notify_time)
    await message.answer('Hi! Send the time in 24-hour format (HH:MM), and you\'ll start '
                         'receiving notifications at that time.')


@router.message(Register.notify_time)
async def set_notify_time(message: Message, state: FSMContext):
    await state.update_data(notify_time=message.text)
    data = await state.get_data()
    notify_time = data.get('notify_time')

    try:
        notify_time = datetime.strptime(notify_time, '%H:%M')
        await state.set_state(Subscribe.base_currency_code)
        await message.answer('Now send the currency code you want to monitor (e.g., USD, EUR, KZT).')
        detail = await register_user(telegram_id=message.from_user.id, notify_time=notify_time.time())
    except ValueError:
        await message.reply('❌ Invalid format! Please enter the time in HH:MM format (e.g., 09:30).')


@router.message(F.text == 'Back')
async def back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text='Back to menu...', reply_markup=await get_actions_markup())


@router.message(Subscribe.base_currency_code)
async def set_base_currency_code(message: Message, state: FSMContext):
    if await check_currency(message.text):
        await state.update_data(base_currency_code=message.text)
        await state.set_state(Subscribe.target_currency_code)
        await message.answer('Please send the currency code of your base currency (e.g., USD, EUR, KZT).')
    else:
        await message.reply('❌ Currency code not found! Please check the code and try again.')


@router.message(Subscribe.target_currency_code)
async def set_target_currency_code(message: Message, state: FSMContext):
    data = await state.get_data()
    base_currency_code = data.get('base_currency_code')
    try:
        if await check_currency(message.text) and base_currency_code != message.text:
            detail = await subscribe_to_currency(message.from_user.id, base_currency_code, message.text)
            await message.answer('✅ You have successfully subscribed!')
            rate = await get_currency(base_currency_code, message.text)
            await message.answer(
                text=f'💱 Current rate: 1 {base_currency_code} - {rate} {message.text}',
                reply_markup=await get_actions_markup()
            )
            await state.clear()
        else:
            await message.reply('❌ Currency code not found or it matches your base currency!')
    except Exception as e:
        await message.answer(
            text=ERROR_MESSAGE,
            reply_markup=await get_back_markup()
        )


@router.message(F.text == 'My subscriptions')
async def my_subscriptions_handler(message: Message):
    response = await get_subscriptions(message.from_user.id)

    if type(response) is list and response:  # might be empty list of subscriptions
        msg = []

        for subscription in response:
            msg.append(f'🔹 {subscription["base_currency_code"]} → {subscription["target_currency_code"]} '
                       f'({subscription["rate"]})')

        msg = '\n'.join(msg)
    elif not response:
        msg = 'No subscriptions found.'
    else:
        msg = ERROR_MESSAGE

    await message.answer(msg)


@router.message(F.text == 'Change notification time')
async def change_notification_time_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Send new notification time!',
        reply_markup=await get_back_markup()
    )
    await state.set_state(Change.notify_time)


@router.message(Change.notify_time)
async def set_new_notification_time(message: Message, state: FSMContext):
    try:
        notify_time = datetime.strptime(message.text, '%H:%M')
        detail = await change_notification_time(message.from_user.id, notify_time.time())
        await message.answer(text='Notification time changed successfully!', reply_markup=await get_actions_markup())
        await state.clear()
    except ValueError:
        await message.reply(
            text='❌ Invalid format! Please enter the time in HH:MM format (e.g., 09:30).',
            reply_markup=await get_back_markup()
        )
    except Exception as e:
        await message.answer(
            text=ERROR_MESSAGE,
            reply_markup=await get_back_markup()
        )


@router.message(F.text == 'New subscription')
async def new_subscription_handler(message: Message, state: FSMContext):
    await message.answer(
        text='Creating new subscription...\nSend the currency code you want to monitor (e.g., USD, EUR, KZT).',
        reply_markup=await get_back_markup()
    )
    await state.set_state(Subscribe.base_currency_code)


@router.message(F.text == 'Delete subscription')
async def delete_subscription_handler(message: Message):
    await message.answer(
        text='Choose subscription to delete',
        reply_markup=await get_subscriptions_markup(message.from_user.id)
    )


@router.callback_query(F.data.startswith('delete:'))
async def delete_subscription_callback(callback: CallbackQuery):
    response = await delete_subscription(callback.from_user.id, callback.data)

    if response == 'Deleted':
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer(text='Deleted successfully!', reply_markup=await get_actions_markup())
    else:
        await callback.message.answer(ERROR_MESSAGE, reply_markup=await get_actions_markup())
        await callback.message.delete()
