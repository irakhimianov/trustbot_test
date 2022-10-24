from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp
from filters import IsNotBanned
from keyboards.default import main_kbd
from database import requests
from states import UserRegistrationState


@dp.message_handler(IsNotBanned(), CommandStart())
async def cmd_start(message: types.Message, session: AsyncSession, state: FSMContext):
    # Command '/start' handler
    user_id = message.from_user.id
    user_is_registered = await requests.user_is_registered(user_id=user_id, session=session)
    if user_is_registered:
        text = 'Добро пожаловать в главное меню чат-бота Управляющей компании УЭР-ЮГ'
        await message.answer(
            text=text,
            reply_markup=main_kbd,
        )
    else:
        text = '<b>☀ Доброго времени суток,</b> бот создан, чтобы обрабатывать заявки и обращения пользователей. ' \
               'Чтобы воспользоваться этим, пришлите для начала Ваше <b>Имя</b> и <b>Фамилию</b>'
        last_message = await message.answer(text=text)
        async with state.proxy() as data:
            data['chat_id'] = message.chat.id
            data['last_message_id'] = last_message.message_id
        await UserRegistrationState.fio.set()
