from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.result import Result
from app.schemas.get_dynamics_params import GetDynamicsParamsDateIntervalSchema, GetDynamicsParamsSchema
from app.schemas.last_dates import LastDatesSchema
from app.schemas.result import ResultSchema, ResultListSchema


class ResultRepository:

    @staticmethod
    async def get_last_dates(session: AsyncSession, date_count: int) -> LastDatesSchema:
        distinct_dates_query = (
            select(Result.date)
            .distinct()
            .order_by(Result.date.desc())
            .limit(date_count)
        )

        dates = []
        for result in await session.execute(distinct_dates_query):
            dates.append(result[0])
        return LastDatesSchema(dates=dates)

    @staticmethod
    async def get_dynamics_by_filters(
            session: AsyncSession,
            params: GetDynamicsParamsDateIntervalSchema
    ) -> ResultListSchema:
        query = select(Result).where(
            and_(
                Result.date >= params.start_date,
                Result.date <= params.end_date,
                *[
                    Result.oil_id == params.oil_id if params.oil_id is not None else True,
                    Result.delivery_type_id == params.delivery_type_id if params.delivery_type_id is not None else True,
                    Result.delivery_basis_id == params.delivery_basis_id if params.delivery_basis_id is not None else True
                ]
            )
        ).order_by(Result.date.desc())
        results = await session.execute(query)
        records = results.scalars().all()
        results_schema = ResultListSchema(
            results=[ResultSchema.model_validate(record, from_attributes=True) for record in records]
        )
        return results_schema

    @staticmethod
    async def get_last_trade_records(session: AsyncSession, params: GetDynamicsParamsSchema) -> ResultListSchema:
        subquery = select(func.max(Result.date)).scalar_subquery()
        query = (
            select(Result)
            .where(and_(
                Result.date == subquery,
                *[
                    Result.oil_id == params.oil_id if params.oil_id is not None else True,
                    Result.delivery_type_id == params.delivery_type_id if params.delivery_type_id is not None else True,
                    Result.delivery_basis_id == params.delivery_basis_id if params.delivery_basis_id is not None else True
                ]
            ))
            .order_by(Result.date.desc())
        )
        results = await session.execute(query)
        results_schema = ResultListSchema(
            results=[ResultSchema.model_validate(result, from_attributes=True) for result in results.scalars().all()]
        )
        return results_schema
