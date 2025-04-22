"""
Этот модуль производит всю необходимую настройку PostgreSQL.
ORM - SQLAlchemy.
"""


from sqlalchemy import Column, Integer, String, Identity
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from config.config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL, echo=True) # echo=True для тестов
Base = declarative_base()

# --- Модели
class PostDBModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, Identity(), primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String)
    body = Column(String)

    def __repr__(self):
        return f'Post {self.id}, user {self.user_id}'


# Модели ---


async def create_tables():
    """
    Создает таблицы если они еще не существуют в базе.
    """

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
