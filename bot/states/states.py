"""
Данный модуль содержит группы состояний для бота.
"""


from aiogram.fsm.state import StatesGroup, State


class APIResponseStates(StatesGroup):
    which_resource = State() # Кнопка
    which_id = State()
