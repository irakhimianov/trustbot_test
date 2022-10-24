from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_to_main = InlineKeyboardButton(
    text='🔙 Назад', callback_data='back_to_main'
)

back_to_main_kbd = InlineKeyboardMarkup(row_width=1)
back_to_main_kbd.add(back_to_main)
