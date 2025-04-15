from aiohttp import web

from aiogram import Dispatcher, Router, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config.config import (
    BOT_TOKEN,

    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    WEBHOOK_URL,
    WEBHOOK_PATH
)

from handlers.default_handlers import default_router


# Создаем бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаем главный роутер
main_router = Router()
main_router.include_router(default_router)

# Создаем диспетчера
dp = Dispatcher()
dp.include_router(main_router)


async def _on_startup(bot_instance: Bot) -> None:
    """
    Функция для инициализации webhook'а боту.

    :param bot_instance: Текущий бот
    """

    await bot_instance.set_webhook(f'{WEBHOOK_URL}/{WEBHOOK_PATH}')


async def _on_shutdown(bot_instance: Bot) -> None:
    """
    Функция для очистки webhook'а у бота.

    :param bot_instance: Текущий бот
    """

    await bot_instance.delete_webhook(drop_pending_updates=True)

async def loader() -> web.AppRunner:

    # Инициализируем webhook
    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)

    # Создаем веб-приложение
    app = web.Application()

    # Создаем обработчик webhook'ов
    webhook_request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_request_handler.register(app, path=WEBHOOK_PATH)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    await site.start()

    return runner
