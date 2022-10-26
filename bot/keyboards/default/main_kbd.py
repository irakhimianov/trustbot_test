from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main_kbd = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
buttons = [
    KeyboardButton(text='📛 Оставить заявку'),
    KeyboardButton(text='📞 Связаться'),
    KeyboardButton(text='⚙ Настройки')
]
main_kbd.add(*buttons)
main_kbd.row(KeyboardButton(text='☎ Полезные контакты'))
