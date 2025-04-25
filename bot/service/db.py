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

# SQLAlchemy
from models.db import (
    engine,

    UserDBModel,
    AddressDBModel,
    GeoDBModel,
    CompanyDBModel,
    PostDBModel,
    UserDBModel,
    CommentDBModel,
    AlbumDBModel,
    PhotoDBModel,
    TodoDBModel
)

# Pydantic
from models.pydantic_api import (
    UserModel,
    UserModelFromDB,

    PostModel,
    PostModelFromDB,

    CommentModel,
    CommentModelFromDB,

    AlbumModel,
    AlbumModelFromDB,

    PhotoModel,
    PhotoModelFromDB,

    TodoModel,
    TodoModelFromDB
)


@injectable
class DBAsyncSessionManager:
    """
    Класс для зависимостей.
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
class _ServiceBase:
    """
    Базовый класс сервисов.
    Инициализирует менеджера сессии
    """

    @autowired
    def __init__(self, db_session_manager: Annotated[DBAsyncSessionManager, Autowired]):
        self.db_session_manager = db_session_manager


@injectable
class _Users(_ServiceBase):
    """
    Сервисный класс для работы с пользователями.
    Реализует метод create_user, который отвечает за сохранение в БД юзера и ID тг-пользователя.
    """

    async def create_user(self, user_pydantic: UserModel, telegram_user_id) -> str:
        async with self.db_session_manager.session() as db:
            try:

                # Получаем данные из связанных Pydantic-моделей
                user_address_geo_api_data = user_pydantic.address.geo.model_dump()
                user_address_api_data = user_pydantic.address.model_dump(exclude={'geo'})
                user_company_api_data = user_pydantic.company.model_dump()
                user_api_data = user_pydantic.model_dump(exclude={'address', 'company'})

                print(f'user_address_geo_api_data - {user_address_geo_api_data}')
                print(f'user_address_api_data - {user_address_api_data}')
                print(f'user_company_api_data - {user_company_api_data}')
                print(f'user_api_data - {user_api_data}')

                # Создаем объекты моделей
                user_address_geo_db = GeoDBModel(**user_address_geo_api_data)
                user_address_db = AddressDBModel(**user_address_api_data, geo=user_address_geo_db)
                user_company_db = CompanyDBModel(**user_company_api_data)
                user_db = UserDBModel(**user_api_data, address=user_address_db, company=user_company_db)

                # Отдельно добавляем Telegram ID
                user_db.telegram_user_id = telegram_user_id

                db.add(user_db)
                logging.info('Выполнил -- db.add(user_db) --')

                # Обновляем объект и получаем поля из БД
                await db.flush()
                logging.info('Выполнил -- db.flush() --')
                await db.refresh(user_db)
                logging.info('Выполнил -- db.refresh(user_db) --')

                # Возвращаем сериализованный JSON объект
                user_validated = UserModelFromDB.model_validate(user_db)
                return user_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении пользователя:\n{e}')
                raise


@injectable
class _Posts(_ServiceBase):
    """
    Сервисный класс для работы с постами.
    Реализует метод create_post, который отвечает за сохранение в БД поста и ID тг-пользователя.
    """

    # async def get_post(self, post_id):
    #     """
    #     Метод для получения поста из БД.
    #     Пока что не задуман для использования.
    #     """
    #     try:
    #         async with self.db_session_manager.session() as db:
    #
    #             # Создаем запрос и получаем данные
    #             query = select(PostDBModel).where(PostDBModel.id == post_id)
    #             result = await db.execute(query)
    #             post = result.scalar_or_none()
    #
    #             if post:
    #                 post_validated = PostModelFromDB.model_validate(post)
    #
    #                 # Возвращаем JSON ответ
    #                 return post_validated.model_dump_json()
    #             else:
    #                 return None
    #     except Exception as e:
    #         logging.error(f'Ошибка при получении поста:\n{e}')
    #         raise

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


@injectable
class _Comments(_ServiceBase):
    """
    Сервисный класс для работы с комментариями.
    Реализует метод create_comment, который отвечает за сохранение в БД комментария и ID тг-пользователя.
    """

    async def create_comment(self, comment_pydantic: CommentModel, telegram_user_id) -> str:
        async with self.db_session_manager.session() as db:
            try:

                # Создаем объект модели
                comment_api_data = comment_pydantic.model_dump()
                comment_db = PostDBModel(**comment_api_data)

                # Отдельно добавляем Telegram ID
                comment_db.telegram_user_id = telegram_user_id

                db.add(comment_db)

                # Обновляем объект и получаем поля из БД
                await db.flush()
                await db.refresh(comment_db)

                # Возвращаем сериализованный JSON объект
                comment_validated = CommentModelFromDB.model_validate(comment_db)
                return comment_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise


@injectable
class _Albums(_ServiceBase):
    """
    Сервисный класс для работы с альбомами.
    Реализует метод create_album, который отвечает за сохранение в БД альбома и ID тг-пользователя.
    """

    async def create_album(self, album_pydantic: AlbumModel, telegram_user_id) -> str:
        async with self.db_session_manager.session() as db:
            try:

                # Создаем объект модели
                album_api_data = album_pydantic.model_dump()
                album_db = AlbumDBModel(**album_api_data)

                # Отдельно добавляем Telegram ID
                album_db.telegram_user_id = telegram_user_id

                db.add(album_db)

                # Обновляем объект и получаем поля из БД
                await db.flush()
                await db.refresh(album_db)

                # Возвращаем сериализованный JSON объект
                album_validated = AlbumModelFromDB.model_validate(album_db)
                return album_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise



@injectable
class _Photos(_ServiceBase):
    """
    Сервисный класс для работы с фотографиями.
    Реализует метод create_photo, который отвечает за сохранение в БД фото и ID тг-пользователя.
    """

    async def create_photo(self, photo_pydantic: PhotoModel, telegram_user_id) -> str:
        async with self.db_session_manager.session() as db:
            try:

                # Создаем объект модели
                photo_api_data = photo_pydantic.model_dump()
                photo_db = PhotoDBModel(**photo_api_data)

                # Отдельно добавляем Telegram ID
                photo_db.telegram_user_id = telegram_user_id

                db.add(photo_db)

                # Обновляем объект и получаем поля из БД
                await db.flush()
                await db.refresh(photo_db)

                # Возвращаем сериализованный JSON объект
                photo_validated = PhotoModelFromDB.model_validate(photo_db)
                return photo_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise


@injectable
class _Todos(_ServiceBase):
    """
    Сервисный класс для работы с заметками.
    Реализует метод create_todo, который отвечает за сохранение в БД заметки и ID тг-пользователя.
    """

    async def create_todo(self, todo_pydantic: TodoModel, telegram_user_id) -> str:
        async with self.db_session_manager.session() as db:
            try:

                # Создаем объект модели
                todo_api_data = todo_pydantic.model_dump()
                todo_db = TodoDBModel(**todo_api_data)

                # Отдельно добавляем Telegram ID
                todo_db.telegram_user_id = telegram_user_id

                db.add(todo_db)

                # Обновляем объект и получаем поля из БД
                await db.flush()
                await db.refresh(todo_db)

                # Возвращаем сериализованный JSON объект
                todo_validated = TodoModelFromDB.model_validate(todo_db)
                return todo_validated.model_dump_json()

            except SQLAlchemyError as e:
                logging.error(f'Ошибка при сохранении поста:\n{e}')
                raise


@injectable
class ServiceDB(_Users, _Posts, _Comments, _Albums, _Photos, _Todos):
    """
    Класс-сервис.
    Объединяет в себе методы для работы со всеми моделями БД, предоставляя единый интерфейс управления.
    Делает это при помощи метода create_obj, который принимает: Данные в pydantic модели, название метода,
    ID пользователя.
    """

    async def create_obj(self, validated_data, resource: str, telegram_user_id: int) -> str:
        if resource.lower() == 'users':
            return await self.create_user(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'posts':
            return await self.create_post(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'comments':
            return await self.create_comment(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'albums':
            return await self.create_album(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'photos':
            return await self.create_photo(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'todos':
            return await self.create_todo(validated_data, telegram_user_id=telegram_user_id)
