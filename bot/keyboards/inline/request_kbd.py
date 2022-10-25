from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .back_to_main import back_to_main


request_kbd = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='📛 Оставить заявку', callback_data='request_leave'),
    InlineKeyboardButton(text='💡 Поделиться предложением', callback_data='request_suggestion'),
]
request_kbd.add(*buttons)
request_kbd.add(back_to_main)
