from aiogram.dispatcher.filters.state import State, StatesGroup


class UserChatState(StatesGroup):
    dialog_start = State()
