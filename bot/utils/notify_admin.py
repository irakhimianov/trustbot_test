import logging

from bot.data.config import ADMIN
from bot.loader import dp


async def on_startup_notify():
    try:
        await dp.bot.send_message(ADMIN, 'Bot started')
    except Exception as e:
        logging.exception(e)
