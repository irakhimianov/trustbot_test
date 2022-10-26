from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from filters import IsAdmin
from keyboards.inline import admin_kbd
from loader import bot, dp


@dp.message_handler(IsAdmin(), commands=['admin'])
async def admin_menu(message: types.Message, state: FSMContext):
    text = 'Приветствую. Вам доступно админ-меню:'
    last_message = await message.answer(text=text, reply_markup=admin_kbd)
    async with state.proxy() as data:
        data['chat_id'] = last_message.chat.id
        data['last_message_id'] = last_message.message_id
