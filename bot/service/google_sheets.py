"""
Данный модуль содержит в себе все классы, зависимости, методы для работы с Google Sheets.

Архитектуру можно представить таким образом:
ABS Class __init__() ---> `Классы для создания записей в листах` ---> Class ServiceGH для передачи в хендлеры.
"""


import logging
import asyncio
from typing import Annotated
from datetime import datetime

from gspread import service_account
from injectable import injectable, autowired, Autowired

from config.config import CREDENTIALS_FILE, SPREADSHEET_ID, SCOPES

# Pydantic
from models.pydantic_api import (
    UserModel,
    PostModel,
    CommentModel,
    AlbumModel,
    PhotoModel,
    TodoModel
)

# GH = Google Sheets

@injectable
class _GHSpreadsheetManager:
    """
    Класс с зависимостями.
    Принимает данные о пользователе, область, ID таблицы.
    Получив по ним таблицу, возвращает лист по указанному имени.
    """

    def __init__(self):
        self.CREDENTIALS_FILE = CREDENTIALS_FILE
        self.SCOPES = SCOPES
        self.SPREADSHEET_ID = SPREADSHEET_ID

    async def _get_spreadsheet_by_id(self):
        client = await asyncio.to_thread(service_account, filename=self.CREDENTIALS_FILE, scopes=self.SCOPES)
        return await asyncio.to_thread(client.open_by_key, self.SPREADSHEET_ID)

    async def get_worksheet_by_name(self, sheet_name: str):
        spreadsheet = await self._get_spreadsheet_by_id()
        return await asyncio.to_thread(spreadsheet.worksheet, sheet_name)


@injectable
class _BaseGHService:
    """
    Базовый класс.
    Предоставляет дочерним классам доступ к таблице и клиенту.
    """

    @autowired
    def __init__(self, gh_spreadsheet_manager: Annotated[_GHSpreadsheetManager, Autowired]):
        self.gh_spreadsheet_manager = gh_spreadsheet_manager


@injectable
class _Users(_BaseGHService):
    """
    Класс для работы с пользователями.
    """

    async def create_user(self, user_model: UserModel, telegram_user_id: int):
        """
        Метод для создания записи данных пользователя в GH.
        Отличается от остальных тем, что делает вложенность - "плоской".
        {company: {name: '...', catchPhrase: '...'}} --> company_name, company_catch_phrase

        :param user_model: Pydantic-модель пользователя.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            user_address_geo_api_data = user_model.address.geo
            user_address_api_data = user_model.address
            user_company_api_data = user_model.company
            user_api_data = user_model

            # Создаем список с данными для заполнения строки
            user_data_list = [
                telegram_user_id,                   # telegram_user_id
                datetime.now().isoformat(),         # created_at

                user_api_data.user_id,              # todo_id
                user_api_data.name,                 # user_id
                user_api_data.username,             # title
                user_api_data.email,                # completed
                user_api_data.phone,                # completed
                user_api_data.website,              # completed

                user_address_api_data.street,       # address_street
                user_address_api_data.suite,        # address_suite
                user_address_api_data.city,         # address_city
                user_address_api_data.zipcode,      # address_zipcode

                user_address_geo_api_data.lat,      # address_geo_lat
                user_address_geo_api_data.lng,      # address_geo_lng

                user_company_api_data.name,         # company_name
                user_company_api_data.catchPhrase,  # company_catchPhrase
                user_company_api_data.bs,           # company_bs
            ]

            # Получаем лист для заполнения и вносим данные
            user_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('users')
            await asyncio.to_thread(user_sheet.append_row, user_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class _Posts(_BaseGHService):
    """
    Класс для работы с постами.
    """

    async def create_post(self, post_model: PostModel, telegram_user_id: int):
        """
        Метод для создания записи данных поста в GH.

        :param post_model: Pydantic-модель поста.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            post_api_data = post_model

            # Создаем список с данными для заполнения строки
            post_data_list = [
                telegram_user_id,           # telegram_user_id
                datetime.now().isoformat(), # created_at
                post_api_data.post_id,      # post_id
                post_api_data.user_id,      # user_id
                post_api_data.title,        # title
                post_api_data.body          # body
            ]

            # Получаем лист для заполнения и вносим данные
            post_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('posts')
            await asyncio.to_thread(post_sheet.append_row, post_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class _Comments(_BaseGHService):
    """
    Класс для работы с комментариями.
    """

    async def create_comment(self, comment_model: CommentModel, telegram_user_id: int):
        """
        Метод для создания записи данных комментария в GH.

        :param comment_model: Pydantic-модель поста.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            comment_api_data = comment_model

            # Создаем список с данными для заполнения строки
            comment_data_list = [
                telegram_user_id,               # telegram_user_id
                datetime.now().isoformat(),     # created_at
                comment_api_data.comment_id,    # comment_id
                comment_api_data.post_id,       # post_id
                comment_api_data.name,          # name
                comment_api_data.email,         # email
                comment_api_data.body           # body
            ]

            # Получаем лист для заполнения и вносим данные
            comment_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('comments')
            await asyncio.to_thread(comment_sheet.append_row, comment_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class _Albums(_BaseGHService):
    """
    Класс для работы с комментариями.
    """

    async def create_album(self, album_model: AlbumModel, telegram_user_id: int):
        """
        Метод для создания записи данных альбома в GH.

        :param album_model: Pydantic-модель поста.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            album_api_data = album_model

            # Создаем список с данными для заполнения строки
            album_data_list = [
                telegram_user_id,           # telegram_user_id
                datetime.now().isoformat(), # created_at
                album_api_data.album_id,    # album_id
                album_api_data.user_id,     # user_id
                album_api_data.title,       # title
            ]

            # Получаем лист для заполнения и вносим данные
            album_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('albums')
            await asyncio.to_thread(album_sheet.append_row, album_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class _Photos(_BaseGHService):
    """
    Класс для работы с комментариями.
    """

    async def create_photo(self, photo_pydantic: PhotoModel, telegram_user_id: int):
        """
        Метод для создания записи данных фотографии в GH.

        :param photo_pydantic: Pydantic-модель поста.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            photo_api_data = photo_pydantic

            # Создаем список с данными для заполнения строки
            photo_data_list = [
                telegram_user_id,               # telegram_user_id
                datetime.now().isoformat(),     # created_at
                photo_api_data.photo_id,        # photo_id
                photo_api_data.album_id,        # album_id
                photo_api_data.title,           # title
                photo_api_data.url,             # url
                photo_api_data.thumbnail_url,   # thumbnail_url
            ]

            # Получаем лист для заполнения и вносим данные
            photo_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('photos')
            await asyncio.to_thread(photo_sheet.append_row, photo_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class _Todos(_BaseGHService):
    """
    Класс для работы с комментариями.
    """

    async def create_todo(self, todo_pydantic: TodoModel, telegram_user_id: int):
        """
        Метод для создания записи данных заметки в GH.

        :param todo_pydantic: Pydantic-модель поста.
        :param telegram_user_id: ID пользователя.
        """

        try:
            # Получаем данные от API
            todo_api_data = todo_pydantic

            # Создаем список с данными для заполнения строки
            todo_data_list = [
                telegram_user_id,               # telegram_user_id
                datetime.now().isoformat(),     # created_at
                todo_api_data.todo_id,          # todo_id
                todo_api_data.user_id,          # user_id
                todo_api_data.title,            # title
                todo_api_data.completed,        # completed
            ]

            # Получаем лист для заполнения и вносим данные
            todo_sheet = await self.gh_spreadsheet_manager.get_worksheet_by_name('todos')
            await asyncio.to_thread(todo_sheet.append_row, todo_data_list)

        except Exception as e:
            logging.error(f'Произошла ошибка при сохранении записи в Google Sheets:\n{e}')
            raise


@injectable
class ServiceGH(_Users, _Posts, _Comments, _Albums, _Photos, _Todos):
    """
    Класс-сервис.
    Объединяет в себе методы для работы со всеми листами Google Sheets, предоставляя единый интерфейс управления.
    Делает это при помощи метода create_obj, который принимает: Название листа, данные в pydantic модели,
    ID пользователя.
    """

    async def create_obj(self, validated_data, resource: str, telegram_user_id: int) -> None:
        if resource.lower() == 'users':
            await self.create_user(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'posts':
            await self.create_post(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'comments':
            await self.create_comment(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'albums':
            await self.create_album(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'photos':
            await self.create_photo(validated_data, telegram_user_id=telegram_user_id)

        elif resource.lower() == 'todos':
            await self.create_todo(validated_data, telegram_user_id=telegram_user_id)
