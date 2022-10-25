from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from filters import IsNotBanned
from loader import bot, dp
from keyboards.default import main_kbd
from keyboards.inline import settings_kbd, cancel_kbd
from database import requests
from states import UserSettingsState
from utils import fio_format_editor, phone_format_editor


@dp.message_handler(IsNotBanned(), text='⚙ Настройки')
async def cmd_settings(message: types.Message, state: FSMContext):
    text = f'Тут Вы сможете поменять <b>Имя</b> и <b>Фамилию</b> в Базе данных нашего бота или же можете поменять ' \
           f'Ваш <b>номер телефона</b>, если Вы изначально вводили что-то неверно. Выберите, что хотите поменять' \
           f' или вернитесь назад в <b><i>главное меню:</i></b>'
    last_message = await message.answer(
        text=text,
        reply_markup=settings_kbd
    )
    async with state.proxy() as data:
        data['chat_id'] = message.chat.id
        data['last_message_id'] = last_message.message_id


@dp.callback_query_handler(text_contains='update_')
@dp.callback_query_handler(text='recall_update_phone')
async def settings_update_info(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('_')[-1]
    if call_data == 'fio':
        text = '🛠 <i>Отправьте свое <b>Имя</b> и <b>Фамилию</b>, чтобы поменять настройки:</i>'
        await UserSettingsState.update_fio.set()
    elif call_data == 'phone':
        text = '🛠 <i>Отправьте свой номер телефона, чтобы поменять настройки:</i>'
        await UserSettingsState.update_phone.set()
    await bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=cancel_kbd
    )
    async with state.proxy() as data:
        data['chat_id'] = call.message.chat.id
        data['last_message_id'] = call.message.message_id
    await bot.answer_callback_query(callback_query_id=call.id)