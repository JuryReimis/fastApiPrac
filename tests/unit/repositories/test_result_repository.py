import datetime

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import async_session
from app.repositories.result_repository import ResultRepository
from app.schemas.get_dynamics_params import GetDynamicsParamsDateIntervalSchema
from app.schemas.last_dates import LastDatesSchema
from app.schemas.result import ResultListSchema


@pytest.fixture(scope="module", autouse=True)
async def sess() -> AsyncSession:
    async with async_session() as sess:
        yield sess


class TestResultRepository:
    CHECK_DATE_COUNT_RESULT = {
        1: LastDatesSchema(dates=[
            datetime.date(2025, 4, 17)
        ]),
        2: LastDatesSchema(dates=[
            datetime.date(2025, 4, 17),
            datetime.date(2025, 4, 16)
        ]),
        3: LastDatesSchema(dates=[
            datetime.date(2025, 4, 17),
            datetime.date(2025, 4, 16),
            datetime.date(2025, 4, 15)
        ])
    }

    CHECK_DYNAMICS_PARAMS = {
        1: GetDynamicsParamsDateIntervalSchema(
            start_date=datetime.date(2025, 4, 17),
            end_date=datetime.date(2025, 4, 17),
            oil_id="PCSZ",
            delivery_type_id="S",
            delivery_basis_id="KII"
        ),
        2: GetDynamicsParamsDateIntervalSchema(
            start_date=datetime.date(2025, 4, 15),
            end_date=datetime.date(2025, 4, 17),
            oil_id="PCSZ",
            delivery_type_id=None,
            delivery_basis_id=None
        ),
        3: GetDynamicsParamsDateIntervalSchema(
            start_date=datetime.date(2025, 4, 15),
            end_date=datetime.date(2025, 4, 17),
            oil_id=None,
            delivery_type_id="A",
            delivery_basis_id=None
        ),
        4: GetDynamicsParamsDateIntervalSchema(
            start_date=datetime.date(2025, 4, 15),
            end_date=datetime.date(2025, 4, 17),
            oil_id=None,
            delivery_type_id=None,
            delivery_basis_id="KII"
        ),
        5: GetDynamicsParamsDateIntervalSchema(
            start_date=datetime.date(2025, 4, 16),
            end_date=datetime.date(2025, 4, 16),
            oil_id=None,
            delivery_type_id="J",
            delivery_basis_id="BTC"
        )
    }

    @pytest.mark.parametrize(
        "date_count, result",
        [
            (1, CHECK_DATE_COUNT_RESULT.get(1)),
            (2, CHECK_DATE_COUNT_RESULT.get(2)),
            (3, CHECK_DATE_COUNT_RESULT.get(3)),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_last_dates(self, sess: AsyncSession, date_count, result):
        repository = ResultRepository()
        response = await repository.get_last_dates(session=sess, date_count=date_count)
        assert response == result

    @pytest.mark.parametrize(
        "filters, results_len",
        [
            (
                    GetDynamicsParamsDateIntervalSchema(
                        start_date=datetime.date(2020, 1, 1),
                        end_date=datetime.datetime.now().date()
                    ),
                    30
            ),
            (
                    CHECK_DYNAMICS_PARAMS.get(1),
                    0
            ),
            (
                    CHECK_DYNAMICS_PARAMS.get(2),
                    1
            ),
            (
                    CHECK_DYNAMICS_PARAMS.get(3),
                    6
            ),
            (
                    CHECK_DYNAMICS_PARAMS.get(4),
                    2
            ),
            (
                    CHECK_DYNAMICS_PARAMS.get(5),
                    1
            )
        ],
        ids=[
            "all_dates",
            "all_dates_no_filters",
            "3_days_one_filter_oil_id",
            "3_days_one_filter_delivery_type_id",
            "3_days_one_filter_delivery_basis_id",
            "one_day_two_filters"
        ]
    )
    @pytest.mark.asyncio
    async def test_get_dynamics_by_filters(self, sess: AsyncSession, filters: GetDynamicsParamsDateIntervalSchema,
                                           results_len: int):
        repository = ResultRepository()
        response = await repository.get_dynamics_by_filters(session=sess, params=filters)
        assert isinstance(response, ResultListSchema)
        assert len(response.results) == results_len
