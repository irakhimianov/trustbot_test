from aiogram import types

from bot.loader import dp


async def set_default_commands():
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустить бота'),
            types.BotCommand('cancel', 'Отмена текущей операции'),
        ]
    )
