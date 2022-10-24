import datetime

from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update

from database import User


async def get_user(user_id: int, session: AsyncSession) -> User:
    user = await session.get(User, user_id)
    return user


async def add_user(
        *,
        user_id: int,
        username: str,
        session: AsyncSession
):
    user = await get_user(user_id=user_id, session=session)
    if user is None:
        user = User(
            telegram_id=user_id,
            username=username,
        )
        session.add(user)
        await session.commit()


async def update_user(
        *,
        user_id: int,
        session: AsyncSession,
        fio: str,
        phone_number: str,
        is_banned: bool,
        is_active: bool,
        is_registered: bool
):
    await session.execute(
        update(User)
        .where(User.telegram_id == user_id)
        .values(
            fio=fio,
            phone_number=phone_number,
            is_banned=is_banned,
            is_active=is_active,
            is_registered=is_registered
        )
    )
    await session.commit()


async def update_user_fio(*, user_id: int, session: AsyncSession, fio: str):
    await session.execute(
        update(User)
        .where(User.telegram_id == user_id)
        .values(fio=fio)
    )
    await session.commit()


async def update_user_phone_number(*, user_id: int, session: AsyncSession, phone_number: str):
    await session.execute(
        update(User)
        .where(User.telegram_id == user_id)
        .values(phone_number=phone_number)
    )
    await session.commit()


async def user_is_banned(user_id: int, session: AsyncSession) -> bool:
    user: User = await get_user(user_id=user_id, session=session)
    if user:
        return bool(user.is_banned)
    return False


async def user_is_active(user_id: int, session: AsyncSession) -> bool:
    user: User = await get_user(user_id=user_id, session=session)
    return bool(user.is_active)


async def user_is_registered(user_id: int, session: AsyncSession) -> bool:
    user: User = await get_user(user_id=user_id, session=session)
    return bool(user.is_registered)
