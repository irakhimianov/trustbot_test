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



@dp.message_handler(state=UserSettingsState.update_fio)
async def update_fio(message: types.Message, session: AsyncSession, state: FSMContext):
    fio = fio_format_editor(fio=message.text)
    data = await state.get_data()
    if not fio:
        text = f'📛<b>Имя</b> и <b>Фамилия</b> должны быть введены через один пробел, и должны быть написаны через ' \
               f'кириллицу. Также должны начинаться с заглавных букв. <b>Учтите формат и попробуйте снова:</b>'
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.edit_message_text(
            text=text,
            chat_id=data['chat_id'],
            message_id=data['last_message_id'],
            reply_markup=cancel_kbd
        )
    else:
        await requests.update_user_fio(
            user_id=message.from_user.id,
            session=session,
            fio=fio
        )
        await bot.delete_message(chat_id=data['chat_id'], message_id=data['last_message_id'])
        text = '✅🛠✅Настройки <b>имени</b> успешно применены!'
        await message.answer(text=text, reply_markup=main_kbd)
        await state.finish()


@dp.message_handler(state=UserSettingsState.update_phone)
async def update_phone(message: types.Message, session: AsyncSession, state: FSMContext):
    phone_number = phone_format_editor(phone_number=message.text)
    data = await state.get_data()
    if not phone_number:
        text = f'📛Номер телефона должен содержать 11 цифр и должен обязательно содержать +7 в начале.' \
               f'<b>Учтите формат и попробуйте снова:</b>'
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.edit_message_text(
            text=text,
            chat_id=data['chat_id'],
            message_id=data['last_message_id'],
            reply_markup=cancel_kbd
        )
    else:
        await requests.update_user_phone_number(
            user_id=message.from_user.id,
            session=session,
            phone_number=phone_number
        )
        await bot.delete_message(chat_id=data['chat_id'], message_id=data['last_message_id'])
        text = '✅🛠✅Настройки <b>номера</b> успешно применены!'
        await message.answer(text=text, reply_markup=main_kbd)
        await state.finish()
