"""
Данный модуль содержит в себе классы-middleware для бота.
"""

from typing import Annotated

from aiogram.types import TelegramObject
from injectable import injectable, autowired, Autowired

from service.db import ServiceDB
from service.google_sheets import ServiceGH


@injectable
class ServicesMiddleware:
    """
    Middleware для загрузки в контекст хендлеров класса-сервиса БД и таблицы Google Sheets.
    """

    @autowired
    def __init__(self, db: Annotated[ServiceDB, Autowired], gh: Annotated[ServiceGH, Autowired]):
        self.db = db # PostgreSQL
        self.gh = gh # Google Sheets

    async def __call__(self, handler, event: TelegramObject, data):
        data['db'] = self.db
        data['gh'] = self.gh
        return await handler(event, data)
