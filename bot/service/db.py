from contextlib import asynccontextmanager
from typing import Annotated
import logging

from injectable import injectable, autowired, Autowired

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from models.db import engine, PostDBModel
from models.pydantic_api import PostModel


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
                query = select(PostDBModel).where(PostDBModel.id == post_id)
                result = await db.execute(query)
                post = result.scalar_or_none()

                if post:
                    post_validated = PostModel.model_validate(post)

                    # Возвращаем JSON ответ
                    return post_validated.model_dump_json()
                else:
                    return None
        except Exception as e:
            logging.error(f'Ошибка при получении поста:\n{e}')
            raise

    async def create_post(self, post_pydantic):
        """
        Метод создающий запись о полученном посте.
        -- все будет переделано --
        :param post_pydantic: Проверенные данные Pydantic.
        :return: JSON-Pydantic модель на основе записи из базы данных, в качестве подтверждения.
        """

        async with self.db_session_manager.session() as db:
            try:
                post_db = PostDBModel(
                    user_id=post_pydantic.user_id,
                    title=post_pydantic.title,
                    body=post_pydantic.body
                )

                db.add(post_db)

                await db.flush()
                await db.refresh(post_db)

                post_validated = PostModel.model_validate(post_db)
                return post_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise
