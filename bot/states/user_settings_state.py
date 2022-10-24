from aiogram.dispatcher.filters.state import State, StatesGroup


class UserSettingsState(StatesGroup):
    update_fio = State()
    update_phone = State()
