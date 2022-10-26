from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.default import main_kbd
from loader import dp, bot


@dp.callback_query_handler(text_contains='cancel', state='*')
async def cmd_cancel(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('_')[-1]
    if await state.get_state():
        data = await state.get_data()
        if data.get('chat_id') and data.get('last_message_id'):
            await bot.delete_message(
                chat_id=data['chat_id'],
                message_id=data['last_message_id']
            )
        await state.finish()
    text = '❌<b>Последняя операция отменена</b>'
    if call_data == 'chat':
        text = '❌📞<b>Диалог с администратором завершен</b>'
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=main_kbd
    )
    await bot.answer_callback_query(callback_query_id=call.id)


@dp.message_handler(commands=['cancel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if await state.get_state():
        data = await state.get_data()
        if data.get('chat_id') and data.get('last_message_id'):
            await bot.delete_message(
                chat_id=data['chat_id'],
                message_id=data['last_message_id']
            )
        await state.finish()
    text = '❌<b>Последняя операция отменена</b>'
    await bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=main_kbd
    )
