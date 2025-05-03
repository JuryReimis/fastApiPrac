from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class GetDynamicsParamsSchema(BaseModel):
    oil_id: Annotated[str | None, Field(
        description="Oil Id",
        max_length=4,
    )] = None

    delivery_type_id: Annotated[str | None, Field(
        description="Delivery Type Id",
        max_length=1
    )] = None

    delivery_basis_id: Annotated[str | None, Field(
        description="Delivery Basis Id",
        max_length=3
    )] = None


class GetDynamicsParamsDateIntervalSchema(GetDynamicsParamsSchema):

    start_date: Annotated[date, Field(
        description="Начальная дата в формате YYYY-MM-DD "
    )]

    end_date: Annotated[date, Field(
        description="Конечная дата в формате YYYY-MM-DD"
    )]

    @model_validator(mode='after')
    def validate_dates(self):
        if self.start_date > self.end_date:
            raise ValueError("Начальная дата не может быть больше конечной")
        if self.start_date > datetime.now().date() or self.end_date > datetime.now().date():
            raise ValueError("Нельзя запрашивать данные из будущего")
        return self
