from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.utils.exceptions import BotBlocked, TelegramAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from data import config
from filters import IsNotBanned, IsAdmin
from loader import bot, dp
from keyboards.inline import cancel_chat_kbd
from database import User, requests
from states import UserChatState


SUPPORTED_TYPES = (
    ContentType.ANIMATION, ContentType.AUDIO, ContentType.PHOTO,
    ContentType.DOCUMENT, ContentType.VIDEO, ContentType.VOICE
)

@dp.message_handler(IsNotBanned(), content_types=SUPPORTED_TYPES, state=UserChatState.dialog_start)
async def media_message(message: types.Message, session: AsyncSession):
    if len(message.caption) > 1000:
        text = '📛 Длина подписи файла более 1000 символов, что не допустимо! Попробуйте еще раз:'
        return await message.reply(text=text)
    user: User = await requests.get_user(user_id=message.from_user.id, session=session)
    text_admin = f'{message.caption}\n\nОт: {user.fio} - {user.phone_number}\n#id{message.from_user.id}'
    await message.copy_to(chat_id=config.ADMIN, caption=text_admin)


@dp.message_handler(IsNotBanned(), state=UserChatState.dialog_start)
async def text_message(message: types.Message, session: AsyncSession):
    if len(message.text) > 4000:
        text = '📛 Длина сообщения более 4000 символов, что не допустимо! Попробуйте еще раз:'
        return await message.reply(text=text)
    user: User = await requests.get_user(user_id=message.from_user.id, session=session)
    text_admin = f'{message.text}\n\nОт: {user.fio} - {user.phone_number}\n#id{message.from_user.id}'
    await message.bot.send_message(chat_id=config.ADMIN, text=text_admin)


@dp.message_handler(IsAdmin(), IsReplyFilter(is_reply=True), content_types=types.ContentTypes.ANY)
async def reply_to_user(message: types.Message):
    try:
        user_id: int = extract_id(message)
    except ValueError as ex:
        return await message.reply(str(ex))
    try:
        await message.copy_to(chat_id=user_id, reply_markup=cancel_chat_kbd)
    except BotBlocked:
        await message.reply(text='Не удалось отправить сообщение адресату, т.к. бот заблокирован на их стороне')
    except TelegramAPIError as ex:
        await message.reply(text=f'Не удалось отправить сообщение адресату! Ошибка: {ex}')


def extract_id(message: types.Message) -> int:
    entities = message.reply_to_message.entities or message.reply_to_message.caption_entities
    if not entities or entities[-1].type != 'hashtag':
        raise ValueError('Не удалось извлечь ID для ответа!')
    hashtag = entities[-1].get_text(message.reply_to_message.text or message.reply_to_message.caption)
    if len(hashtag) < 4 or not hashtag[3:].isdigit():
        raise ValueError('Некорректный ID для ответа!')
    return int(hashtag[3:])
