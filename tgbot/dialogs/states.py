from aiogram.fsm.state import State, StatesGroup


class Menu(StatesGroup):
    start = State()


class Survay(StatesGroup):
    start = State()
    instruction = State()
    birth_day = State()
    full_name = State()
    age = State()
    phone = State()
    surgery = State()
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()
    question6 = State()
    question7 = State()
    question8 = State()
    question9 = State()
    question10 = State()
    question11 = State()
    question12 = State()
    question13 = State()
    question14 = State()
    imt_height = State()
    imt_weight = State()
    wash = State()
    self_assessment = State()
    survay_result = State()


class AdminPanel(StatesGroup):
    start = State()
    ozenka = State()
    add_admin = State()
