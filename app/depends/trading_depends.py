from typing import Annotated

from fastapi import Query

from app.schemas.get_dynamics_params import GetDynamicsParamsSchema


async def get_dynamics_params(
        oil_id: Annotated[str | None, Query(
            description="Oil Id",
            max_length=4,
        )] = None,
        delivery_type_id: Annotated[str | None, Query(
            description="Delivery Type Id",
            max_length=1
        )] = None,
        delivery_basis_id: Annotated[str | None, Query(
            description="Delivery Basis Id",
            max_length=3
        )] = None
):
    return GetDynamicsParamsSchema(oil_id=oil_id, delivery_type_id=delivery_type_id,
                                   delivery_basis_id=delivery_basis_id)
