from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import ADMIN
from filters import IsNotBanned
from database import User
from loader import bot, dp
from keyboards.default import main_kbd
from keyboards.inline import request_kbd, back_to_main_kbd
from database import requests
from states import UserLeaveRequestState
from utils import fio_format_editor, phone_format_editor


# to do keyboard, mediagroup handler, caption length

@dp.message_handler(state=UserLeaveRequestState.address)
async def request_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    text = '<i><b>Шаг 2/3</b></i>. 🖼Прикрепите фотографию или видео к своей заявке или пропустите этот пункт:'
    await message.answer(text=text)
    await UserLeaveRequestState.media.set()


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserLeaveRequestState.media)
async def request_media(message: types.Message, state: FSMContext):
    # print(bool(message.video))

    if message.content_type not in ['photo', 'video']:
        text = f'⛔️📛 В данном пункте нужно обязательно отправить <b>фотографию</b> или <b>видео</b> ' \
               f'в виде медиа-сообщения. <i><b>Попробуйте еще раз</b>:</i>'
        await message.answer(text=text)
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=message.message_id
        )
    else:
        if message.photo:
            media = f'photo {message.photo[-1].file_id}'
        elif message.video:
            media = f'video {message.video.file_id}'

        async with state.proxy() as data:
            data['media'] = media
        text = '<i><b>Шаг 3/3</b></i>. 📛Напишите причину обращения в подробностях:'
        await message.answer(text=text)
        await UserLeaveRequestState.reason.set()


@dp.message_handler(state=UserLeaveRequestState.reason)
async def request_reason(message: types.Message, session: AsyncSession, state: FSMContext):
    async with state.proxy() as data:
        data['reason'] = message.text
    user: User = await requests.get_user(user_id=message.from_user.id, session=session)
    username = user.username if user.username else 'Пользователь'
    data = await state.get_data()
    text = '✅<b>Жалоба отправлена администрации.</b> <i>Спасибо за Ваше обращение!</i>'
    await message.answer(text=text)
    await state.finish()

    text_admin = f'<b>⛔Поступила новая жалоба</b>\n<a href="tg://user?id={user.telegram_id}">{username}</a>\n' \
                 f'<i><b>Имя и Фамилия:</b></i> {user.fio}\n' \
                 f'<i><b>Номер телефона:</b></i> {user.phone_number}\n' \
                 f'<i><b>Адрес:</b></i> {data["address"]}\n' \
                 f'<i><b>Содержание:</b></i> {data["reason"]}'

    if data['media']:
        media, file_id = data['media'].split()
        if media == 'photo':
            await bot.send_photo(chat_id=ADMIN, photo=file_id, caption=text_admin)
        elif media == 'video':
            await bot.send_video(chat_id=ADMIN, video=file_id, caption=text_admin)
    else:
        await bot.send_message(chat_id=ADMIN, text=text_admin)
