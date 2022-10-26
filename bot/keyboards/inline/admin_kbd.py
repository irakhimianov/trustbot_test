from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database import User, requests
from utils import Paginator


admin_kbd = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton(text='✉ Рассылка', callback_data='broadcast'),
    InlineKeyboardButton(text='👤 Пользователи', callback_data='get_users_list')
]
admin_kbd.add(*buttons)


def user_list_kbd(users) -> Paginator:
    kb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for user in users:
        user: User
        buttons.append(
            InlineKeyboardButton(
                text=f'{user.username} {user.fio}',
                callback_data=f'get_user_id_{user.telegram_id}')
        )
    kb.add(*buttons)
    paginator = Paginator(data=kb, size=5)
    return paginator


def user_ban_kbd(user: User) -> InlineKeyboardMarkup:
    text, call_data = ('✅ Разбанить', 'unban') if user.is_banned else ('❌ Забанить', 'ban')
    buttons = [
        InlineKeyboardButton(text=text, callback_data=f'{call_data}_{user.telegram_id}'),
        InlineKeyboardButton(text='🔙 Назад', callback_data='to_users_list')
    ]
    kbd = InlineKeyboardMarkup(row_width=1)
    kbd.add(*buttons)
    return kbd


to_users_list_kbd = InlineKeyboardMarkup(row_width=1)
to_users_list_kbd.add(
    InlineKeyboardButton(text='🔙 Назад', callback_data='to_users_list')
)
