from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, Field


class ResultSchema(BaseModel):
    id: int

    exchange_product_id: Annotated[str, Field(max_length=50)]

    exchange_product_name: Annotated[str, Field(max_length=500)]

    oil_id: Annotated[str, Field(max_length=4)]

    delivery_basis_id: Annotated[str, Field(max_length=3)]

    delivery_type_id: Annotated[str, Field(max_length=1)]

    delivery_basis_name: Annotated[str, Field(max_length=255)]

    volume: int

    total: int

    count: int

    date: date

    created_on: datetime

    updated_on: datetime


class ResultListSchema(BaseModel):

    results: Annotated[list[ResultSchema], Field(title="Список результатов запроса")]
