from aiogram.dispatcher.filters.state import State, StatesGroup


class UserLeaveRequestState(StatesGroup):
    address = State()
    media = State()
    reason = State()
