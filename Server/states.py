from aiogram.fsm.state import StatesGroup, State


class Reg(StatesGroup):
    fio = State()
    sex = State()
    born = State()
    residence = State()
    education = State()
    course = State()
    profession = State()
    salary = State()
    hard_work = State()
    mid_work = State()
    art_work = State()
    other_work = State()
    tools = State()
    language = State()
    phone = State()
    email = State()
    citizenship = State()
    wallet = State()
    is_driver = State()
    transport = State()
    is_millitary = State()
    other_info = State()

