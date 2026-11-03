from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    age = State()
    district = State()
    subcultures = State()
    photo = State()
    description = State()
    gender = State()
    looking_for = State()
    confirm = State()
