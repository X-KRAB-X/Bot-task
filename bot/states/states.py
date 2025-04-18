from aiogram.fsm.state import StatesGroup, State


class APIResponseStates(StatesGroup):
    which_url = State() # Кнопка
    which_resource = State()
