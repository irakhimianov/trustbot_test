from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot


@dp.callback_query_handler(text_contains='cancel', state='*')
async def cmd_cancel(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('_')[-1]
    if await state.get_state():
        data = await state.get_data()
        if data['chat_id'] and data['last_message_id']:
            await bot.delete_message(
                chat_id=data['chat_id'],
                message_id=data['last_message_id']
            )
        await state.finish()
    text = 'Последняя операция отменена'
    if call_data == 'dialog':
        text = '<b>❌📞 Диалог с администратором завершен</b>'
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=text
    )