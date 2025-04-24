import logging

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from keyboard.api_get_keyboard import api_get_keyboard, only_cancel_keyboard, test_keyboard


test_router = Router(name='test_router')



@test_router.message(Command(commands=['test']))
async def test_command_handler(message: Message):
    logging.info('Вошел в функцию test_command_handler')
    await message.answer('Вот тебе клавиатура', reply_markup=test_keyboard)


@test_router.inline_query(F.data == 'testing')
async def test_callback_handler(callback: CallbackQuery):
    await callback.answer()
    logging.info('Вошел в функцию test_callback_handler')
    await callback.message.answer('Тестовое сообщение, запрос сработал')


@test_router.inline_query()
async def all_callback_handler(callback: CallbackQuery):
    logging.info(f'Получен коллбэк с данными {callback.data}')
    await callback.answer()
