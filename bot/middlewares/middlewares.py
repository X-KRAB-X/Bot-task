"""
Данный модуль содержит в себе классы-middleware для бота.
"""

from aiogram.types import TelegramObject
from injectable import load_injection_container, injectable, InjectionContainer

from service.db import Posts

class InjectableMiddleware:
    """
    Middleware для загрузки контейнера injectable.
    Дабавляет в контекст хендлера классы-сервисы БД.
    """

    async def __call__(self, handler, event: TelegramObject, dict):
        if not InjectionContainer.is_loaded():
            load_injection_container()

        data['posts'] = injectable.get(Posts)
        return await handler(event, data)
