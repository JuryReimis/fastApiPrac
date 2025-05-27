import asyncio
from asyncio import WindowsSelectorEventLoopPolicy

import pytest

from app.config import settings
from app.models.database import async_engine, BaseModel, get_async_session, async_session
from app.models.result import Result
from app.schemas.result import ResultSchema
from tests.test_data.db_data import test_data


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():

    if settings.MODE == "TEST":
        async with async_engine.connect() as conn:
            await conn.run_sync(BaseModel.metadata.drop_all)
            await conn.run_sync(BaseModel.metadata.create_all)
            await conn.commit()
            print("Все таблицы созданы")

        async with async_session() as sess:
            for data in test_data.get('results'):
                # valid_data = ResultSchema(**data)
                sess.add(Result(**data))
            await sess.commit()
    else:
        raise ValueError("Не предоставлены необходимые тестовые параметры. MODE в .env.test должен быть TEST")






