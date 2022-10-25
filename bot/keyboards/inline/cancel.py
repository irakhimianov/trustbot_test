from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


cancel_kbd = InlineKeyboardMarkup(row_width=1)
cancel_button = InlineKeyboardButton(text='Отмена ❌', callback_data='cancel')
cancel_kbd.add(cancel_button)

dialog_cancel_kbd = InlineKeyboardMarkup(row_width=1)
dialog_cancel_button = InlineKeyboardButton(text='❌📞 Завершить диалог', callback_data='cancel_dialog')
dialog_cancel_kbd.add(dialog_cancel_button)

skip_kbd = InlineKeyboardMarkup(row_width=1)
