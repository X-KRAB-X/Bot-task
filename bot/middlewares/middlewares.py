"""
Данный модуль содержит в себе классы-middleware для бота.
"""

from typing import Annotated

from aiogram.types import TelegramObject
from injectable import injectable, autowired, Autowired

from service.db import ServiceDB


@injectable
class DBMiddleware:
    """
    Middleware для загрузки в контекст хендлеров класса-сервиса БД.
    """

    @autowired
    def __init__(self, db: Annotated[ServiceDB, Autowired]):
        self.db = db

    async def __call__(self, handler, event: TelegramObject, data):
        data['db'] = self.db
        return await handler(event, data)
