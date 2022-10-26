from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from filters import IsNotBanned
from loader import bot, dp
from keyboards.inline import request_kbd, back_to_main_kbd, skip_back_kbd
from states import UserSuggestionState, UserLeaveRequestState


@dp.message_handler(IsNotBanned(), text='📛 Оставить заявку')
async def cmd_leave_request(message: types.Message, state: FSMContext):
    text = '📛👇📛 <i>Выберите категорию, по которой Вы хотите оставить заявку в УК:</i>'
    last_message = await message.answer(
        text=text,
        reply_markup=request_kbd
    )
    async with state.proxy() as data:
        data['chat_id'] = message.chat.id
        data['last_message_id'] = last_message.message_id


@dp.callback_query_handler(text_contains='request_')
async def request_info(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('_')[-1]
    data = await state.get_data()
    if call_data == 'leave':
        text = '<i><b>Шаг 1/3</b></i>. 📓 Напишите адрес или ориентир проблемы (улицу, номер дома, ' \
               'подъезд, этаж и квартиру) или пропустите этот пункт:'
        await UserLeaveRequestState.address.set()
        kbd = skip_back_kbd(skip=True, to_main=True)
    elif call_data == 'suggestion':
        text = '💡 <i><b>Распишите Ваше предложение в подробностях: (Добавьте фотографию, если есть)</b></i>'
        await UserSuggestionState.suggestion.set()
        kbd = back_to_main_kbd
    await bot.edit_message_text(
        text=text,
        chat_id=data['chat_id'],
        message_id=data['last_message_id'],
        reply_markup=kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)
