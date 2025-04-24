import logging

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

default_router = Router(name='default_router')


@default_router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(message: Message):
    await message.answer(text='Привет тебе!', parse_mode=None)


@default_router.message.register(Command(commands=['help']), StateFilter(None))
async def help_handler(message: Message):
    await message.answer(text='Я нахожу в разработке, умею только здороваться.', parse_mode=None)


@default_router.message.register()
async def delete_message_handler(message: Message):
    """
    Удаляет сообщение пользователя.
    Реагирует на бессмысленные сообщения вне состояний, либо когда этого не ожидается.
    """

    try:
        await message.delete()
    except Exception as e:
        logging.error(f'Ошибка при удалении сообщения:\n{e}')
