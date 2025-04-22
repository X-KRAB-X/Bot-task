"""
Данный модуль содержит в себе классы-middleware для бота.
"""

from typing import Annotated

from aiogram.types import TelegramObject
from injectable import injectable, autowired, Autowired

from service.db import Posts


@injectable
class InjectableMiddleware:
    """
    Middleware для загрузки контейнера injectable.
    Дабавляет в контекст хендлера классы-сервисы БД.
    """

    @autowired
    def __init__(
            self,
            posts: Annotated[Posts, Autowired],
            # Здесь еще классы будут
    ):
        self.posts = posts

    async def __call__(self, handler, event: TelegramObject, data):

        data['posts'] = self.posts
        return await handler(event, data)
