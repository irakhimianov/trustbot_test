from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cancel_kbd = InlineKeyboardMarkup(row_width=1)
cancel_button = InlineKeyboardButton(text='Отмена ❌', callback_data='cancel')
cancel_kbd.add(cancel_button)

cancel_chat_kbd = InlineKeyboardMarkup(row_width=1)
cancel_chat_button = InlineKeyboardButton(text='❌📞 Завершить диалог', callback_data='cancel_chat')
cancel_chat_kbd.add(cancel_chat_button)
