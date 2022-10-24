import asyncio
import logging

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

import handlers
from loader import dp, bot
from utils import on_startup_notify, set_default_commands
from middlewares import DBMiddleware, UserMiddleware
from database import Base


async def on_startup():
    logging.basicConfig(
        format=u'%(filename)s:%(lineno)-d #%(levelname)-16s [%(asctime)s] %(message)s',
        level=logging.INFO
    )
    # DB
    logging.info('DB connecting...')
    db_engine = create_async_engine(url='sqlite+aiosqlite:///db.db')
    async with db_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    db_factory = sessionmaker(bind=db_engine, class_=AsyncSession, expire_on_commit=False)
    logging.info('DB connected!')

    # middlewares
    logging.info('Setting up middlewares...')
    dp.setup_middleware(DBMiddleware(db_factory))
    dp.setup_middleware(UserMiddleware())

    logging.info('Everything is ready to launch!')
    # Set default commands (/start and /help)
    await set_default_commands()

    # Notify admin that the bot has started
    await on_startup_notify()
    await dp.skip_updates()
    await dp.start_polling()


async def on_shutdown():
    logging.info('Shutting down...')
    await dp.storage.close()
    await dp.storage.wait_closed()
    bot_session = await bot.get_session()
    await bot_session.close()


async def main():
    try:
        await on_startup()
    finally:
        await on_shutdown()


if __name__ == '__main__':
    # Launch bot
    asyncio.get_event_loop().run_until_complete(main())
