"""
Архитектура выглядит таким образом:
ABS Class __init__ ---> `Классы для создания записей в таблицах` ---> Class Service для передачи в хендлеры.
"""


from contextlib import asynccontextmanager
from typing import Annotated
import logging

from injectable import injectable, autowired, Autowired

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from models.db import engine, PostDBModel
from models.pydantic_api import PostModel, PostModelFromDB


@injectable
class DBAsyncSessionManager:
    """
    Сервисный класс.
    Инициализирует и возвращает асинхронную сессию.
    """

    def __init__(self):
        self.AsyncSessionLocal = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def session(self):
        """
        Контекстный менеджер сессии.
        Представляет собой функцию-генератор.
        Возвращает сессию и ловит ошибки, после чего закрывает соединение.
        """

        async with self.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise
            finally:
                await session.close()

# TODO Сделать общий класс для настройки

@injectable
class Posts:
    """
    Сервисный класс.
    Служит для выполнения запросов к таблице БД - -?
    """

    @autowired
    def __init__(self, db_session_manager: Annotated[DBAsyncSessionManager, Autowired]):
        self.db_session_manager = db_session_manager

    async def get_post(self, post_id):
        """
        Метод для получения поста из БД.
        Пока что не задуман для использования.
        """
        try:
            async with self.db_session_manager.session() as db:

                # Создаем запрос и получаем данные
                query = select(PostDBModel).where(PostDBModel.id == post_id)
                result = await db.execute(query)
                post = result.scalar_or_none()

                if post:
                    post_validated = PostModelFromDB.model_validate(post)

                    # Возвращаем JSON ответ
                    return post_validated.model_dump_json()
                else:
                    return None
        except Exception as e:
            logging.error(f'Ошибка при получении поста:\n{e}')
            raise

    async def create_post(self, post_pydantic: PostModel, telegram_user_id) -> str:
        """
        Метод получает модель Pydantic, сохраняет запись в БД и возвращает новую Pydantic модель
        :param post_pydantic: Проверенные данные Pydantic.
        :param telegram_user_id: ID пользователя, который отправил сообщение боту.

        :return: JSON-Pydantic модель на основе записи из базы данных, в качестве подтверждения.
        """

        async with self.db_session_manager.session() as db:
            try:

                # Создаем объект модели
                post_api_data = post_pydantic.model_dump()
                post_db = PostDBModel(**post_api_data)

                # Отдельно добавляем Telegram ID
                post_db.telegram_user_id = telegram_user_id

                db.add(post_db)

                # Обновляем объект и получаем поля из БД
                await db.flush()
                await db.refresh(post_db)

                # Возвращаем сериализованный JSON объект
                post_validated = PostModelFromDB.model_validate(post_db)
                return post_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise
