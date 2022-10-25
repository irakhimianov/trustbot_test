from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from loader import dp, bot
from filters import IsNotBanned
from keyboards.default import main_kbd


@dp.callback_query_handler(IsNotBanned(), text='back_to_main', state='*')
async def back_to_main(call: types.CallbackQuery, state: FSMContext):
    if await state.get_state():
        await state.finish()
    await bot.answer_callback_query(callback_query_id=call.id)
    await call.message.delete()
    text = 'Добро пожаловать в главное меню чат-бота Управляющей компании УЭР-ЮГ'
    await call.message.answer(
        text=text,
        reply_markup=main_kbd,
    )
