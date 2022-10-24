from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .back_to_main import back_to_main


settings_kbd = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='🛠 Поменять имя', callback_data='update_fio'),
    InlineKeyboardButton(text='🛠 Сменить номер', callback_data='update_phone'),
]
settings_kbd.add(*buttons)
settings_kbd.add(back_to_main)
