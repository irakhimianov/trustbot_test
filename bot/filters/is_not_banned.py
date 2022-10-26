import aiogram
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from bot.database.requests import *
from loader import bot


class IsNotBanned(BoundFilter):
    async def check(self, interaction: types.Message | types.CallbackQuery):
        session: AsyncSession = ctx_data.get()['session']
        if isinstance(interaction, types.Message):
            interaction: types.Message
            user_id = interaction.from_user.id
        elif isinstance(interaction, types.CallbackQuery):
            interaction: types.CallbackQuery
            user_id = interaction.message.from_user.id
        banned: bool = await user_is_banned(user_id=user_id, session=session)
        if banned:
            await bot.send_message(text='Вы забанены', chat_id=user_id)
        else:
            return not banned
