import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.fixture
async def mock_redis(mocker):
    mock_client = AsyncMock()
    mock_client.get.return_value = None
    mock_client.set.return_value = None
    mock_client.flush_db.return_value = None
    mocker.patch('app.views.trading_views.cache_service._client', new=mock_client)
    return mock_client


@pytest.fixture
async def mock_session(mocker):
    session = AsyncMock()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    session.execute.return_value = mock_result
    mock_result.scalars.return_value = mock_scalars

    return session


@pytest.fixture
async def client(mock_redis):
    async with AsyncClient(transport=ASGITransport(app), base_url='http://test') as ac:
        yield ac

