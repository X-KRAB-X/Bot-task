"""
Этот модуль производит всю необходимую настройку PostgreSQL.
ORM - SQLAlchemy.
"""

from datetime import datetime

from sqlalchemy import Integer, String, Identity, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import create_async_engine

from config.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL, echo=True) # echo=True для тестов
Base = declarative_base()

# --- Модели
class BaseDBModel(Base):
    """
    Данный абстрактный класс определяет поля, который присущи всем таблицам БД,
    т.е. информацию о пользователе и времени запроса.

    Все далее созданные классы наследуют эти аттрибуты(поля).
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    telegram_user_id: Mapped[int] = mapped_column(Integer, index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())


class UserDBModel(BaseDBModel):
    __tablename__ = 'users'

    user_id: Mapped[int]
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    website: Mapped[str]

    address: Mapped['AddressDBModel'] = relationship(back_populates='user')
    company: Mapped['CompanyDBModel'] = relationship(back_populates='user')

    def __repr__(self):
        return f'User {self.user_id}'


class AddressDBModel(Base):
    """
    Данная модель не нацелена на отслеживание истории действий пользователя, поэтому не наследуется от `BaseDBModel`
    """

    __tablename__ = 'addresses'

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    street: Mapped[str] = mapped_column(String)
    suite: Mapped[str] = mapped_column(String)
    city: Mapped[str] = mapped_column(String)
    zipcode: Mapped[str] = mapped_column(String)
    geo: Mapped['GeoDBModel'] = relationship(back_populates='address')

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserDBModel'] = relationship(back_populates='address')


class GeoDBModel(Base):
    """
    Данная модель не нацелена на отслеживание истории действий пользователя, поэтому не наследуется от `BaseDBModel`
    """

    __tablename__ = 'geos'

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    lat: Mapped[float] = mapped_column(Float)
    lng: Mapped[float] = mapped_column(Float)

    address_id: Mapped[int] = mapped_column(ForeignKey('addresses.id'))
    address: Mapped['AddressDBModel'] = relationship(back_populates='geo')


class CompanyDBModel(Base):
    """
    Данная модель не нацелена на отслеживание истории действий пользователя, поэтому не наследуется от `BaseDBModel`
    """

    __tablename__ = 'companies'

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String)
    catchPhrase: Mapped[str] = mapped_column(String)
    bs: Mapped[str] = mapped_column(String)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['UserDBModel'] = relationship(back_populates='company')


class PostDBModel(BaseDBModel):
    __tablename__ = 'posts'

    post_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'Post {self.post_id}, user {self.user_id}'


class CommentDBModel(BaseDBModel):
    __tablename__ = 'comments'

    post_id: Mapped[int] = mapped_column(Integer, index=True)
    comment_id: Mapped[int] = mapped_column(Integer, index=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    body: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'Comment {self.comment_id}, post {self.post_id}'


class AlbumDBModel(BaseDBModel):
    __tablename__ = 'albums'

    user_id: Mapped[int] = mapped_column(Integer, index=True)
    album_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'Album {self.album_id}, user {self.user_id}'


class PhotoDBModel(BaseDBModel):
    __tablename__ = 'photos'

    album_id: Mapped[int] = mapped_column(Integer, index=True)
    photo_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)
    url: Mapped[str] = mapped_column(String)
    thumbnail_url: Mapped[str] = mapped_column(String)

    def __repr__(self):
        return f'Photo {self.photo_id}, album {self.album_id}'


class TodoDBModel(BaseDBModel):
    __tablename__ = 'todos'

    user_id: Mapped[int] = mapped_column(Integer, index=True)
    todo_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String)
    completed: Mapped[bool] = mapped_column(Boolean)

    def __repr__(self):
        return f'Todo {self.todo_id}, user {self.user_id}'


async def create_tables():
    """
    Создает таблицы если они еще не существуют в базе.
    """

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
