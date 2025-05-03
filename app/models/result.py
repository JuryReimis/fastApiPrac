from datetime import datetime

from sqlalchemy import String, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import BaseModel


class Result(BaseModel):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)

    exchange_product_id: Mapped[str] = mapped_column(String(50), index=True)

    exchange_product_name: Mapped[str] = mapped_column(String(500))

    oil_id: Mapped[str] = mapped_column(String(4))

    delivery_basis_id: Mapped[str] = mapped_column(String(3))

    delivery_type_id: Mapped[str] = mapped_column(String(1))

    delivery_basis_name: Mapped[str] = mapped_column(String(255))

    volume: Mapped[int] = mapped_column()

    total: Mapped[int] = mapped_column()

    count: Mapped[int] = mapped_column()

    date: Mapped[datetime] = mapped_column(Date(), nullable=False)

    created_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_on: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(),
                                                 onupdate=func.now())
