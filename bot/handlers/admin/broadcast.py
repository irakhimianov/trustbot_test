import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database import User, requests
from filters import IsAdmin
from keyboards.inline import cancel_kbd, admin_kbd
from loader import dp, bot
from states import BroadcastState


@dp.callback_query_handler(IsAdmin(), text='broadcast')
async def broadcast(call: types.CallbackQuery, state: FSMContext):
    """
    Broadcast callback handler
    :param call:
    :return:
    """
    data = await state.get_data()
    text = 'Введите текст для рассылки:'
    await bot.edit_message_text(
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        text=text,
        reply_markup=cancel_kbd
    )
    await BroadcastState.text.set()
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(IsAdmin(), state=BroadcastState.text)
async def broadcast_text(message: types.Message, session: AsyncSession, state: FSMContext):
    """
    Handler to get the broadcast text
    :param message:
    :param state:
    :param session:
    :return:
    """
    logging.info(f'Broadcast by {message.from_user.id}')
    users = await requests.get_users(session)
    users = [user for user in users]

    for user in users:
        user: User
        try:
            await bot.send_message(chat_id=user.telegram_id, text=message.text)
            if not user.is_active:
                await requests.activate_user(user_id=user.telegram_id, session=session)
        except Exception as e:
            await requests.deactivate_user(user_id=user.telegram_id, session=session)
            logging.error(f'{user.telegram_id} - {e}')
    await state.finish()
    await message.answer(text='Рассылка осуществлена', reply_markup=admin_kbd)
