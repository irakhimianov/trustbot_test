from aiogram import types

from bot.loader import dp


async def set_default_commands():
    # Pop-up tips when '/' is typed in chat-window with bot
    await dp.bot.set_my_commands(
        [
            types.BotCommand('start', 'Start bot'),
            types.BotCommand('help', 'What this bot can do'),
        ]
    )
