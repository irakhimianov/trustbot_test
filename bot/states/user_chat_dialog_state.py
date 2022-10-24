from aiogram.dispatcher.filters.state import State, StatesGroup


class UserChatDialogState(StatesGroup):
    dialog_start = State()
