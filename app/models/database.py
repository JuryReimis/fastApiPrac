from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config import DATABASE_URL


class BaseModel(AsyncAttrs, DeclarativeBase):
    pass


async_engine = create_async_engine(DATABASE_URL)

async_session = async_sessionmaker(bind=async_engine, class_=AsyncSession)


async def get_async_session():
    async with async_session() as sess:
        yield sess
