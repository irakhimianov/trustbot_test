from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .back_to_main import back_to_main


request_kbd = InlineKeyboardMarkup(row_width=2)
buttons = [
    InlineKeyboardButton(text='📛 Оставить заявку', callback_data='request_leave'),
    InlineKeyboardButton(text='💡 Поделиться предложением', callback_data='request_suggestion'),
]
request_kbd.add(*buttons)
request_kbd.add(back_to_main)


def skip_back_kbd(*, skip: bool = False, back: bool = False, to_main: bool = False):
    kbd = InlineKeyboardMarkup(row_width=1)
    skip_btn = InlineKeyboardButton(text='Пропустить', callback_data='request_skip')
    back_btn = InlineKeyboardButton(text='Назад', callback_data='request_back')
    if skip and back:
        buttons = (skip_btn, back_btn)
    elif skip and to_main:
        buttons = (skip_btn, back_to_main)
    else:
        buttons = (back_btn,)
    kbd.add(*buttons)
    return kbd
