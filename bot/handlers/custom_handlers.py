import logging
import json

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State

from api.api import get_json_response
from config.config import API_URL
from states.states import APIResponseStates


custom_router = Router(name='custom_router')

# TODO Добавить валидацию для вводимых полей
@custom_router.message(Command(commands=['get']))
async def get_command_handler(message: Message, state: State):

    # Устанавливаем состояние
    await state.set_state(APIResponseStates.which_url)

    await message.answer(f'Отправляем запрос по URL {API_URL, 'posts/1'}\nКакой путь?')


@custom_router.message(APIResponseStates.which_url)
async def get_setting_path_handler(message: Message, state: State):

    # Сохраняем полученный ответ - путь
    await state.update_data(which_url=message.text)

    # Устанавливаем след. состояние
    await state.set_state(APIResponseStates.which_resource)

    await message.answer('Какой id ресурса? От 1 до 100')


@custom_router.message(APIResponseStates.which_url)
async def get_response_data_handler(message: Message, state: State):

    # Сохраняем и получаем указанный путь и id ресурса
    state_data = await state.update_data(which_resource=message.text)

    await message.answer('Отправляю запрос и собираю данные..')
    try:
        logging.info('Отправляю запрос на URL {API_URL}{which_url}/{which_resource}'.format(
            API_URL=API_URL,
            which_url=state_data['which_url'],
            which_resource=state_data['which_resource']
        ))

        data = await get_json_response(
            API_URL,
            state_data['which_url'] + '/' + state_data['which_resource']
        )
        serialized_data = json.dumps(data, indent=4)

    except Exception as e:
        logging.error(f'Произошла ошибка при запросе:\n{e}')
        await message.answer('Произошла ошибка при запросе, проверьте логи')
    else:
        await message.answer(f'Было получен ответ JSON:\n{serialized_data}')

    # Очищаем состояние
    await state.clear()
