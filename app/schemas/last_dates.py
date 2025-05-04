from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class LastDatesSchema(BaseModel):

    dates: Annotated[list[date], Field(title="Список дат")]
