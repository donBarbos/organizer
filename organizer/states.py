from aiogram.dispatcher.filters.state import State, StatesGroup


class Note(StatesGroup):
    text = State()
    time = State()


class WeeklyNote(StatesGroup):
    text = State()
    day = State()
    time = State()
