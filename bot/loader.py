from aiohttp import web

from aiogram import Dispatcher, Router, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


from config.config import (
    BOT_TOKEN,

    WEBHOOK_URL,
    WEBHOOK_PATH
)
from handlers.default_handlers import default_router


async def on_startup(bot_instance: Bot) -> None:
    """
    Функция для инициализации webhook'а боту.

    :param bot_instance: Текущий бот
    """

    await bot_instance.set_webhook(f'{WEBHOOK_URL}/{WEBHOOK_PATH}')


# Создаем главный роутер
main_router = Router()
main_router.include_router(default_router)

# Создаем диспетчера
dp = Dispatcher()
dp.include_router(main_router)

# Инициализируем webhook
dp.startup.register(on_startup)

# Создаем бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаем веб-приложение
app = web.Application()
