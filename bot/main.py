import asyncio
import logging
from aiohttp import web

from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from loader import bot, dp, app

from config.config import (
    WEB_SERVER_HOST,
    WEB_SERVER_PORT,

    WEBHOOK_PATH
)


async def main():
    # await dp.start_polling(bot)

    # Создаем обработчик webhook'ов
    webhook_request_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_request_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    asyncio.run(main())
