from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import JSON, ForeignKey, Numeric, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass



class Devices(Base):
    __tablename__ = "Devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_type: Mapped[str]
    brand: Mapped[str]
    location: Mapped[str]
    ip: Mapped[str]
    ser_number: Mapped[str] = mapped_column(unique=True)
    capacity_device: Mapped[dict] = mapped_column(JSON)
    supply_id: Mapped[int] = mapped_column(ForeignKey("supplies.id"))
    user_id: Mapped[id] = mapped_column(ForeignKey("UserProfile.id"), nullable=False)



class Supply(Base):
    __tablename__ = "supplies"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    device_type: Mapped[str]
    brand: Mapped[str]
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    supplier: Mapped[str]
    data_supply: Mapped[datetime] = mapped_column(server_default=func.now())


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
