import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

default_router = Router(name='default_router')

@default_router.message(Command(commands=['start']))
async def start_handler(message: Message):
    await message.answer(text='Привет тебе!', parse_mode=None)


@default_router.message(Command(commands=['help']))
async def start_handler(message: Message):
    await message.answer(text='Я нахожу в разработке, умею только здороваться.', parse_mode=None)