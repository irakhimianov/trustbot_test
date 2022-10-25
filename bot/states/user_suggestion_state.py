from aiogram.dispatcher.filters.state import State, StatesGroup


class UserSuggestionState(StatesGroup):
    suggestion = State()
