"""
Модуль содержит в себе модели Pydantic 2.0+ для валидации ответов API
Данные взяты с https://jsonplaceholder.typicode.com/
"""

# Todo Сделать валидацию для многих полей. Для телефона и email использовать regex
from datetime import datetime

from pydantic import BaseModel, validator, Field, ConfigDict

from models.db import PhotoDBModel


class _DBMixin(BaseModel):
    """
    Класс-примесь
    Содержит поля, которые создаются в БД
    """

    id: int
    telegram_user_id: int
    created_at: datetime


class _UsersAddressGeoModel(BaseModel):
    lat: float
    lng: float

    model_config = ConfigDict(from_attributes=True)


class _UsersAddressModel(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: _UsersAddressGeoModel

    model_config = ConfigDict(from_attributes=True)


class _UsersCompanyModel(BaseModel):
    name: str
    catchPhrase: str
    bs: str

    model_config = ConfigDict(from_attributes=True)


class UserModel(BaseModel):
    user_id: int = Field(alias='id')
    name: str
    username: str
    email: str
    address: _UsersAddressModel
    phone: str
    website: str
    company: _UsersCompanyModel

    model_config = ConfigDict(from_attributes=True)


class UserModelFromDB(UserModel, _DBMixin):
    user_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов


class PostModel(BaseModel):
    post_id: int = Field(alias='id')
    user_id: int
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)


class PostModelFromDB(PostModel, _DBMixin):
    post_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов


class CommentsModel(BaseModel):
    post_id: int
    comment_id: int = Field(alias='id')
    name: str
    email: str
    body: str

    model_config = ConfigDict(from_attributes=True)


class CommentModelFromDB(CommentsModel, _DBMixin):
    comment_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов


class AlbumModel(BaseModel):
    user_id: int
    album_id: int = Field(alias='id')
    title: str

    model_config = ConfigDict(from_attributes=True)


class AlbumModelFromDB(AlbumModel, _DBMixin):
    album_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов


class PhotoModel(BaseModel):
    album_id: int
    photo_id: int = Field(alias='id')
    title: str
    url: str
    thumbnail_url: str

    model_config = ConfigDict(from_attributes=True)


class PhotoModelFromDB(PhotoModel, _DBMixin):
    photo_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов


class TodoModel(BaseModel):
    user_id: int
    todo_id: int = Field(alias='id')
    title: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class TodoModelFromDB(TodoModel, _DBMixin):
    todo_id: int = Field() # Лишаем поле alias='id' во избежание конфликтов
