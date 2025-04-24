import logging

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

default_router = Router(name='default_router')


@default_router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(message: Message, bot: Bot):
    await message.answer(text='Привет тебе!', parse_mode=None)


@default_router.message(Command(commands=['help']), StateFilter(None))
async def help_handler(message: Message, bot: Bot):
    await message.answer(text='Я нахожу в разработке, умею только здороваться.', parse_mode=None)


@default_router.message(StateFilter(None))
async def delete_message_handler(message: Message):
    """
    Удаляет сообщение пользователя.
    Реагирует на бессмысленные сообщения вне состояний, либо когда этого не ожидается.
    """

    logging.info(f'Активировалось `delete_message_handler`')
    try:
        await message.delete()
    except Exception as e:
        logging.error(f'Ошибка при удалении сообщения:\n{e}')
