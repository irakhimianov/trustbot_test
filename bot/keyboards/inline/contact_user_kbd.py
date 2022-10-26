from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .back_to_main import back_to_main

contact_user_kbd = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton(text='📞 Перезвоните мне', callback_data='contact_recall'),
    InlineKeyboardButton(text='📞 Свяжитесь со мной в чат-боте', callback_data='contact_chat'),
]
contact_user_kbd.add(*buttons)
contact_user_kbd.add(back_to_main)

recall_kbd = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton(text='✅ Да', callback_data='recall_confirm'),
    InlineKeyboardButton(text='🛠 Изменить номер телефона', callback_data='recall_update_phone')
]
recall_kbd.add(*buttons)
