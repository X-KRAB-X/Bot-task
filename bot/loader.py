from aiohttp import web
import logging

from aiogram import Dispatcher, Router, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config.config import (
    BOT_TOKEN,

    WEB_SERVER_HOST,
    WEB_SERVER_PORT,
    WEBHOOK_URL,
    WEBHOOK_PATH,

    BOT_COMMANDS
)

from handlers.default_handlers import default_router
from handlers.custom_handlers import custom_router

# БД
from models.db import create_tables
from middlewares.middlewares import ServicesMiddleware

# Google Sheets
from models.google_sheets import create_google_sheets

from injectable import load_injection_container

logging.basicConfig(level='DEBUG')

# Создаем бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаем главный роутер
main_router = Router()

main_router.include_router(custom_router)
main_router.include_router(default_router)


# Создаем диспетчера
dp = Dispatcher()
dp.include_router(main_router)


async def _set_webhook(bot_instance: Bot) -> None:
    """
    Функция для инициализации webhook'а боту.

    :param bot_instance: Текущий бот
    """
    try:
        await bot_instance.set_webhook(
            f'{WEBHOOK_URL}{WEBHOOK_PATH}',
            allowed_updates=["message", "callback_query"] # Очень важно, чтобы тг мог отправлять callback_query
        )
        logging.info(f'Установлен путь для вебхука: {WEBHOOK_URL}{WEBHOOK_PATH}')
    except Exception as e:
        logging.error(f'Произошла ошибка при установке вебхука:\n{e}')


async def clear_webhook(bot_instance: Bot) -> None:
    """
    Функция для очистки webhook'а у бота.

    :param bot_instance: Текущий бот
    """
    logging.info(f'Удален вебхук: {WEBHOOK_URL}{WEBHOOK_PATH}')
    try:
        await bot_instance.delete_webhook(drop_pending_updates=True)
    except Exception as e:
        logging.error(f'Произошла ошибка при очистке вебхука:\n{e}')


async def loader() -> web.AppRunner:
    """
    Сборка и настройка всех частей бота:
    Веб-приложение, Вебхук для бота, БД, Листы Google Sheets, команды.
    """

    # Загрузка команд в бота
    await bot.set_my_commands(BOT_COMMANDS)

    # Загрузка контейнера для зависимостей
    load_injection_container()

    # Создаем таблицы БД если их нет
    # await create_tables()

    # Создаем листы в Google Sheets
    # await create_google_sheets()

    # Регистрация middleware БД
    dp.message.outer_middleware(ServicesMiddleware())

    # Инициализируем webhook
    await _set_webhook(bot_instance=bot)

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
