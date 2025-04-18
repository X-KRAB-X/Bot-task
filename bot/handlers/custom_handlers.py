import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from api.api import get_json_response
from config.config import API_URL

custom_router = Router(name='custom_router')


@custom_router.message(Command(commands=['get']))
async def get_request_handler(message: Message):
    await message.answer('Отправляю запрос и собираю данные..')

    try:
        logging.info(f'Отправляю запрос на URL {API_URL + 'posts/1'}')
        data = await get_json_response(API_URL, 'posts/1')
        print(type(data))
    except Exception as e:
        logging.error(f'Произошла ошибка при запросе:\n{e}')
        await message.answer('Произошла ошибка при запросе, проверьте логи')
    else:
        await message.answer(f'Было получен ответ JSON:\n{data}')
