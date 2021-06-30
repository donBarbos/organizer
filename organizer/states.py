from aiogram.dispatcher.filters.state import StatesGroup, State


class Note(StatesGroup):
    text = State()
    time = State()


class WeeklyNote(StatesGroup):
    text = State()
    day = State()
    time = State()
