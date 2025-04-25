import logging

from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

default_router = Router(name='default_router')


@default_router.message(Command(commands=['start']), StateFilter(None))
async def start_handler(message: Message):
    await message.answer(text='Привет тебе! Можешь написать /help или выбрать команду снизу.', parse_mode=None)


@default_router.message(Command(commands=['help']), StateFilter(None))
async def help_handler(message: Message):
    await message.answer(text='Привет!\nУ меня есть такой список команд:\n'
                              '/start - Поздороваюсь с тобой еще раз!\n'
                              '/help - Сейчас именно она. Показываю справку.\n'
                              '/get - Отправляю запрос по API.\n'
                              '1.Даю на выбор параметры, из которых будет составлен URL.\n'
                              '2.Сохраняю результат запроса в базе данных.\n'
                              '3.Показываю что получилось, в формате JSON.'
                         )


@default_router.message()
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
