from datetime import date
from decimal import Decimal
from typing import Any
from sqlalchemy import JSON, ForeignKey
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

class Device(Base):
    __tablename__ = "Devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_type: Mapped[str]
    brand: Mapped[str]
    location: Mapped[str] = "storage"
    ip: Mapped[str]
    ser_number: Mapped[str] = mapped_column(unique=True)
    capacity_device: Mapped[str] = mapped_column(JSON)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"))

