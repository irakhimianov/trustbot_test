from aiogram.dispatcher.filters.state import State, StatesGroup


class BroadcastState(StatesGroup):
    text = State()
