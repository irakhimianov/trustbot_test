from aiogram.dispatcher.filters.state import State, StatesGroup


class UserRegistrationState(StatesGroup):
    fio = State()
    phone_number = State()
