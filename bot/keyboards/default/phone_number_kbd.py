from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


phone_number_kbd = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

buttons = [
    KeyboardButton('📱 Отправить номер телефона', request_contact=True),
]
phone_number_kbd.add(*buttons)
