import asyncio

from aiogram import Dispatcher, Router, Bot

from config.config import BOT_TOKEN
from handlers.default_handlers import default_router

dp = Dispatcher()

main_router = Router()
main_router.include_router(default_router)

bot = Bot(token=BOT_TOKEN)
