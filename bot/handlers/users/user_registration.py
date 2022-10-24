from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from filters import IsNotBanned
from loader import bot, dp
from keyboards.default import main_kbd, phone_number_kbd
from database import requests
from states import UserRegistrationState
from utils import fio_format_editor, phone_format_editor
from .start import cmd_start


@dp.message_handler(IsNotBanned(), state=UserRegistrationState.fio)
async def registration_fio(message: types.Message, state: FSMContext):
    # message.text fio check
    fio = fio_format_editor(fio=message.text)
    if not fio:
        text = f'📛 <b>Имя</b> и <b>Фамилия</b> должны быть введены через один пробел, и должны быть написаны через ' \
               f'кириллицу. Также должны начинаться с заглавных букв. <b>Учтите формат и попробуйте снова:</b>'
    else:
        text = 'Теперь отправьте Ваш номер телефона через +7 следующим сообщением'
        await UserRegistrationState.next()
        async with state.proxy() as data:
            data['fio'] = fio

    data = await state.get_data()
    chat_id = data['chat_id']
    last_message_id = data['last_message_id']

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    await bot.edit_message_text(
        text=text,
        chat_id=chat_id,
        message_id=last_message_id
    )


@dp.message_handler(IsNotBanned(), state=UserRegistrationState.phone_number)
async def registration_phone_number(message: types.Message, session: AsyncSession, state: FSMContext):
    # message.text phone_number check
    data = await state.get_data()
    chat_id = data['chat_id']
    last_message_id = data['last_message_id']

    phone_number = phone_format_editor(phone_number=message.text)
    if not phone_number:
        text = f'📛 Номер телефона должен содержать 11 цифр и должен обязательно содержать +7 в начале.' \
               f'<b>Учтите формат и попробуйте снова:</b>'
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=last_message_id
        )
    else:
        text = 'Вы успешно зарегестрированы'
        data['phone_number'] = phone_number
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=last_message_id
        )
        await requests.update_user(
            user_id=message.from_user.id,
            session=session,
            fio=data['fio'],
            phone_number=data['phone_number'],
            is_banned=False,
            is_active=True,
            is_registered=True
        )
        await state.finish()
        await cmd_start(message=message, session=session, state=state)