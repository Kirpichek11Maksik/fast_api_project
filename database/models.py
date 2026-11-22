from datetime import date
from decimal import Decimal
from typing import Any

from sqlalchemy import Enum as SAEnum, Numeric
from sqlalchemy.orm import DeclarativeMeta, Mapped, declared_attr, mapped_column, declarative_base, DeclarativeBase

class Base(DeclarativeBase):
    pass


class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    device_type: Mapped[str]
    brand: Mapped[str]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    supplier: Mapped[str]
    data_supply: Mapped[date]