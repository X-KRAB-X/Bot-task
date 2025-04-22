"""
Модуль содержит в себе модели Pydantic 2.0+ для валидации ответов API
Данные взяты с https://jsonplaceholder.typicode.com/
"""

# Todo Сделать валидацию для многих полей. Для телефона и email использовать regex
from pydantic import BaseModel, validator, Field, ConfigDict


class _UsersAddressGeoModel(BaseModel):
    lat: float
    lng: float


class _UsersAddressModel(BaseModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: _UsersAddressGeoModel


class _UsersCompanyModel(BaseModel):
    name: str
    catchPhrase: str
    bs: str


class UsersModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    address: _UsersAddressModel
    phone: str
    website: str
    company: _UsersCompanyModel


class PostModel(BaseModel):
    id: int
    user_id: int
    title: str
    body: str

    model_config = ConfigDict(from_attributes=True)


class CommentsModel(BaseModel):
    post_id: int
    id: int
    name: str
    email: str
    body: str


class AlbumsModel(BaseModel):
    user_id: int
    id: int
    title: str


class PhotosModel(BaseModel):
    albumId: int
    id: int
    title: str
    url: str
    thumbnailUrl: str


class TodosModel(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool
