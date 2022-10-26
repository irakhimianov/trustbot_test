from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database import requests
from filters import IsAdmin
from keyboards.inline import user_list_kbd, user_ban_kbd, to_users_list_kbd
from loader import bot, dp


@dp.callback_query_handler(IsAdmin(), text='get_users_list')
@dp.callback_query_handler(IsAdmin(), text='to_users_list')
async def get_users_list(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    users = await requests.get_users(session)
    users = [user for user in users]
    paginator = user_list_kbd(users=users)
    args, kwargs = paginator.paginator_handler()
    dp.register_callback_query_handler(*args, **kwargs)
    text = '👤 Список пользователей:'
    await bot.edit_message_text(
        text=text,
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        reply_markup=paginator()
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='get_user_id_')
async def get_user(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    user_id = int(call.data.split('_')[-1])
    user = await requests.get_user(user_id=user_id, session=session)
    username = f'@{user.username} - ' if user.username else ''
    text = f'<u><b>Пользователь:</b></u>\n' \
           f'<u>Telegram id:</u>{user.telegram_id}\n' \
           f'<i>{username}{user.fio} - {user.phone_number}</i>\n' \
           f'Зарегистрирован: {user.registration_date.strftime("%d-%m-%Y %H:%M")}'
    await bot.edit_message_text(
        text=text,
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        reply_markup=user_ban_kbd(user)
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='unban_')
async def unban_user(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    user_id = int(call.data.split('_')[-1])
    await requests.unban_user(user_id=user_id, session=session)
    text = '✅ Пользователь разбанен'
    await bot.edit_message_text(
        text=text,
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        reply_markup=to_users_list_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(IsAdmin(), text_contains='ban_')
async def ban_user(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    data = await state.get_data()
    user_id = int(call.data.split('_')[-1])
    await requests.ban_user(user_id=user_id, session=session)
    text = '❌ Пользователь забанен'
    await bot.edit_message_text(
        text=text,
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        reply_markup=to_users_list_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)
