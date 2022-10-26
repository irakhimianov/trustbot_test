from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from data.config import ADMIN
from database import User, requests
from keyboards.default import main_kbd
from loader import bot, dp
from states import UserSuggestionState


@dp.message_handler(content_types=types.ContentTypes.ANY, state=UserSuggestionState.suggestion)
async def user_suggestion(message: types.Message, session: AsyncSession, state: FSMContext):
    if message.content_type not in ['text', 'photo']:
        return await message.answer(text='📛⛔ Предложение должно содержать фото или текст:')
    else:
        if message.photo:
            if len(message.caption) > 1000:
                text = '📛 Длина подписи файла более 1000 символов, что не допустимо! Попробуйте еще раз:'
                return await message.reply(text=text)
            else:
                async with state.proxy() as data:
                    data['photo'] = message.photo[-1].file_id
                    data['text'] = message.caption
        else:
            if len(message.text) > 4000:
                text = '📛 Длина сообщения более 4000 символов, что не допустимо! Попробуйте еще раз:'
                return await message.reply(text=text)
            else:
                async with state.proxy() as data:
                    data['text'] = message.text
        # TODO вынести в отдельную функцию

        user: User = await requests.get_user(user_id=message.from_user.id, session=session)
        username = user.username if user.username else 'Пользователь'
        data = await state.get_data()
        text = '✅💡<b>Идея принята и передана администрации.</b> Спасибо за <i>Ваше обращение!</i>'
        await message.answer(text=text, reply_markup=main_kbd)
        await state.finish()

        text_admin = f'<b>💡Поступило новое предложение</b>\n<a href="tg://user?id={user.telegram_id}">{username}</a>\n'\
                     f'<i><b>Имя и Фамилия:</b></i> {user.fio}\n' \
                     f'<i><b>Номер телефона:</b></i> {user.phone_number}\n' \
                     f'<i><b>Содержание:</b></i> {data.get("text", "Отсутствует")}'
        if data.get('photo'):
            await bot.send_photo(chat_id=ADMIN, photo=data['photo'], caption=text_admin)
            # await bot.send_photo(chat_id=SUGGESTION_CHAT, photo=data['photo'], caption=text_admin)
        else:
            await bot.send_message(chat_id=ADMIN, text=text_admin)
            # await bot.send_message(chat_id=SUGGESTION_CHAT, text=text_admin)

