from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message):
    # Command '/help' handler
    await message.answer(text='Template help message')
