import datetime

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.models.database import get_async_session
from app.schemas.get_dynamics_params import GetDynamicsParamsSchema

RESULTS_LIST = [
    {
        "id": 114242,
        "exchange_product_id": "DSC5BIN065J",
        "exchange_product_name": "ДТ ЕВРО сорт C (ДТ-Л-К5) минус 5, ст. Биклянь (ст. отправления ОТП)",
        "oil_id": "DSC5",
        "delivery_basis_id": "BIN",
        "delivery_type_id": "J",
        "delivery_basis_name": "ст. Биклянь",
        "volume": 585,
        "total": 34534500,
        "count": 6,
        "date": "2025-04-16",
        "created_on": "2025-04-17T14:11:13.051285+03:00",
        "updated_on": "2025-04-17T14:11:13.051285+03:00"
    },
    {
        "id": 114243,
        "exchange_product_id": "DSC5BTC065J",
        "exchange_product_name": "ДТ ЕВРО сорт C (ДТ-Л-К5) минус 5, БП (б.т.ц.) Осенцы (ст. отправления ОТП)",
        "oil_id": "DSC5",
        "delivery_basis_id": "BTC",
        "delivery_type_id": "J",
        "delivery_basis_name": "БП (б.т.ц.) Осенцы",
        "volume": 3575,
        "total": 217519575,
        "count": 36,
        "date": "2025-04-16",
        "created_on": "2025-04-17T14:11:13.051285+03:00",
        "updated_on": "2025-04-17T14:11:13.051285+03:00"
    }
]


class TestTradingViews:

    @pytest.mark.parametrize(
        "return_dates, input_count, status_code",
        [
            ([
                 (datetime.date(2025, 5, 26),),
                 (datetime.date(2025, 5, 27),)
             ],
             2,
             200),
            ([
                 (datetime.date(2025, 5, 26),),
                 (datetime.date(2025, 5, 27),),
                 (datetime.date(2025, 5, 26),),
                 (datetime.date(2025, 5, 27),),
                 (datetime.date(2025, 5, 26),)
             ],
             5,
             200),
            ([

             ],
             None,
             422)
        ]
    )
    @pytest.mark.asyncio
    async def test_last_trading_dates(self, client, mock_session, return_dates, input_count, status_code):
        mock_session.execute.return_value = return_dates
        app.dependency_overrides[get_async_session] = lambda: mock_session
        response = await client.get(f'/last-trading-dates', params={'query': input_count})
        assert response.status_code == status_code
        if response.status_code == 200:
            assert response.json().get('dates') == list(map(lambda d: d[0].isoformat(), return_dates))

    @pytest.mark.parametrize(
        'start_date, end_date, params, status_code',
        [
            ("2025-04-15", "2025-05-17", {
            },
             200),
            ("2025-06-15", "2025-05-17", {
            },
             422),
            ("2025-04-15", "2025-05-17", {
                'delivery_type_id': 'A',
                'delivery_basis_id': 'AAA',
                'oil_id': 'AAAA'
            },
             200),
            ("2025-04-15", "2025-05-17", {
                'oil_id': '',
                'delivery_basis_id': '',
                'delivery_type_id': ''
            },
             200),
            ("2025-04-15", "2025-05-17", {
                'oil_id': 'sdfgfsd',
                'delivery_basis_id': 'sdfsdfdsf',
                'delivery_type_id': 'sdfdsasdfasdfsdfsddfsdfdsfasdf'
            },
             422),
            ("", "", {
            },
             422)
        ],
        ids=[
            "only_dates",
            "start_date_>_end_date",
            "full_correct_query",
            "all_query_params_empty",
            "incorrect_query_params",
            "no_dates"
        ]
    )
    @pytest.mark.asyncio
    async def test_get_dynamics(self, client, mock_redis, mock_session, start_date: str, end_date: str,
                                params: dict, status_code: int):
        mock_session.execute.scalars.all = RESULTS_LIST
        app.dependency_overrides[get_async_session] = lambda: mock_session
        response = await client.get('/dynamics',
                                    params={'start_date': start_date, 'end_date': end_date, **params})
        assert response.status_code == status_code

    @pytest.mark.parametrize(
        "params, status_code",
        [
            ({
                 'delivery_type_id': 'A',
                 'delivery_basis_id': 'AAA',
                 'oil_id': 'AAAA'
             },
             200),
            ({
             },
             200),
            ({
                 'oil_id': 'sdfgfsd',
                 'delivery_basis_id': 'sdfsdfdsf',
                 'delivery_type_id': 'sdfdsasdfasdfsdfsddfsdfdsfasdf'
             },
             422),
        ],
        ids=[
            "full_correct_query",
            "all_query_params_empty",
            "incorrect_query_params",
        ]
    )
    @pytest.mark.asyncio
    async def test_get_trading_results(self, client, mock_session, params: dict, status_code: int):
        mock_session.execute.scalars.all = RESULTS_LIST
        app.dependency_overrides[get_async_session] = lambda: mock_session
        response = await client.get('/last_trading_day', params={**params})
        print(response.request, response.status_code, response.json())
        assert response.status_code == status_code
