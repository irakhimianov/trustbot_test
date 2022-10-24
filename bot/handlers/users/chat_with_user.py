from aiogram import types
from aiogram.dispatcher.filters import IsReplyFilter
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.exceptions import BotBlocked, TelegramAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from data import config
from filters import IsNotBanned, IsAdmin
from loader import bot, dp
from keyboards.default import main_kbd
from keyboards.inline import contact_user_kbd, recall_kbd, cancel_kbd
from database import User, requests
from states import UserChatDialogState
from utils import fio_format_editor, phone_format_editor


@dp.message_handler(IsNotBanned(), state=UserChatDialogState.dialog_start)
async def chat_dialog(message: types.Message, session: AsyncSession):
    if len(message.text) > 4000:
        text = 'К сожалению, длина этого сообщения превышает допустимый размер. Попробуйте ещё раз.'
        return await message.reply(text=text)
    db_user = await requests.get_user(user_id=message.from_user.id, session=session)
    text = f'{message.text}\n\nОт: {db_user.fio} - {db_user.phone_number}\n#id{message.from_user.id}'
    await message.bot.send_message(
        chat_id=config.ADMIN,
        text=text
    )


@dp.message_handler(IsAdmin(), IsReplyFilter(is_reply=True), content_types=types.ContentTypes.ANY)
async def reply_to_user(message: types.Message):
    try:
        user_id = extract_id(message)
    except ValueError as ex:
        return await message.reply(str(ex))
    try:
        await message.copy_to(user_id)
    except BotBlocked:
        await message.reply('Не удалось отправить сообщение адресату, т.к. бот заблокирован на их стороне')
    except TelegramAPIError as ex:
        await message.reply(f'Не удалось отправить сообщение адресату! Ошибка: {ex}')


def extract_id(message: types.Message) -> int:
    entities = message.reply_to_message.entities or message.reply_to_message.caption_entities
    if not entities or entities[-1].type != 'hashtag':
        raise ValueError('Не удалось извлечь ID для ответа!')
    hashtag = entities[-1].get_text(message.reply_to_message.text or message.reply_to_message.caption)
    if len(hashtag) < 4 or not hashtag[3:].isdigit():
        raise ValueError('Некорректный ID для ответа!')
    return hashtag[3:]
