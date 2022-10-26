from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data import config
from filters import IsNotBanned
from loader import bot, dp
from keyboards.default import main_kbd
from keyboards.inline import contact_user_kbd, recall_kbd, cancel_chat_kbd
from database import User, requests
from states import UserChatState


@dp.message_handler(IsNotBanned(), text='📞 Связаться')
async def cmd_contact(message: types.Message, state: FSMContext):
    text = f'👇 <i>Выберите способ связи из нижеперечисленного списка:</i>'
    last_message = await message.answer(
        text=text,
        reply_markup=contact_user_kbd
    )
    async with state.proxy() as data:
        data['chat_id'] = message.chat.id
        data['last_message_id'] = last_message.message_id


@dp.callback_query_handler(text_contains='contact_')
async def contact_way(call: types.CallbackQuery, session: AsyncSession):
    call_data = call.data.split('_')[-1]

    if call_data == 'recall':
        db_user: User = await requests.get_user(user_id=call.from_user.id, session=session)
        phone_number = db_user.phone_number
        text = f'<b>Это Ваш верный номер телефона</b> <code>{phone_number}</code>? ' \
               f'<i>Если да, нажмите соответствующую кнопку, <b>если нет,</b></i>' \
               f'впишите свой актуальный номер телефона здесь'
        kbd = recall_kbd
        # state
    elif call_data == 'chat':
        text = f'✅📞✅Добрый день! Я - диспетчер управляющей компании "УЭР-ЮГ", готов помочь Вам. ' \
               f'Напишите, пожалуйста интересующий Вас вопрос и ожидайте'
        kbd = cancel_chat_kbd
        await UserChatState.dialog_start.set()

    await bot.edit_message_text(
        text=text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.callback_query_handler(text='recall_confirm')
async def contact_recall(call: types.CallbackQuery, session: AsyncSession, state: FSMContext):
    if await state.get_state():
        await state.finish()
    user: User = await requests.get_user(user_id=call.from_user.id, session=session)
    text_to_admin = f'Запрос <u>перезвонить</u> от <b>{user.fio}</b> <code>{user.phone_number}</code>'
    text = '✅<b>Отлично!</b> Наш диспетчер перезвонит Вам в ближайшее время.'
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await call.message.answer(text=text, reply_markup=main_kbd)
    await bot.send_message(chat_id=config.ADMIN, text=text_to_admin)
    # await bot.send_message(chat_id=config.RECALL_CHAT, text=text_to_admin)
    await bot.answer_callback_query(callback_query_id=call.id)
