"""
Данный модуль содержит в себе классы-middleware для бота.
"""

from typing import Annotated

from aiogram.types import TelegramObject
from injectable import injectable, autowired, Autowired

from service.db import ServiceDB


@injectable
class InjectableMiddleware:
    """
    Middleware для загрузки контейнера injectable.
    Дабавляет в контекст хендлера классы-сервисы БД.
    """

    @autowired
    def __init__(
            self,
            db: Annotated[ServiceDB, Autowired],
            # Здесь еще классы будут
    ):
        self.db = db

    async def __call__(self, handler, event: TelegramObject, data):

        data['db'] = self.db
        return await handler(event, data)
