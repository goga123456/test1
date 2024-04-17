from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    razdel = State()
    kard = State()
    paid = State()
    transactions = State()
    registration = State()
    monitoring_pays = State()
    beep = State()
    my_home = State()
    bonus = State()
    chatting_with_operator = State()
