from datetime import date
from typing import Annotated

from fastapi import Query, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.depends.trading_depends import get_dynamics_params
from app.models.database import get_async_session
from app.repositories.result_repository import ResultRepository
from app.schemas.get_dynamics_params import GetDynamicsParamsDateIntervalSchema, GetDynamicsParamsSchema
from app.schemas.result import ResultSchema


router = APIRouter(prefix='')


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
DynamicsParamsDep = Annotated[GetDynamicsParamsSchema, Depends(get_dynamics_params)]


@router.get(
    '/last-trading-dates',
    name="Получить список дат последних торговых дней"
)
async def get_last_trading_dates(
        session: SessionDep,
        query: Annotated[int, Query(
            title="Количество последних торговых дней",
            description="Ожидается количество торговых дней, которое необходимо отобразить в отчете",
            gt=0,
            example=1,
        )] = None
):
    repository = ResultRepository()
    dates = await repository.get_last_dates(session, query)
    return dates


@router.get(
    '/dynamics',
    name="Получить список торгов за заданный период"
)
async def get_dynamics(
        session: SessionDep,
        start_date: Annotated[date, Query(
            description="Начальная дата в формате YYYY-MM-DD ",
            example="2020-01-01"
        )],
        end_date: Annotated[date, Query(
            description="Конечная дата в формате YYYY-MM-DD",
            example="2025-01-01"
        )],
        params: DynamicsParamsDep
) -> list[ResultSchema]:
    params = GetDynamicsParamsDateIntervalSchema(
        start_date=start_date,
        end_date=end_date,
        **params.model_dump()
    )
    repository = ResultRepository()
    records = await repository.get_dynamics_by_filters(session, params)
    return records


@router.get('/last_trading_day', name="Получить данные за последний зафиксированный день торгов")
async def get_trading_results(
        session: SessionDep,
        params: DynamicsParamsDep
) -> list[ResultSchema]:
    repository = ResultRepository()
    results = await repository.get_last_trade_records(session, params)
    return results
