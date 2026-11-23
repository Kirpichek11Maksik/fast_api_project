from datetime import date  
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from schema.supply_models import DeviceType, Brand


class Capacity_Device(BaseModel):
    human: int = Field(ge=300, le=3000)
    photo: int = Field(ge=300, le=3000)
    card: int = Field(ge=300, le=3000)
    event: int = Field(ge=150000, le=150000)


class Device(BaseModel):
    device_type: DeviceType
    brand: Brand
    location : str = "storage"
    ip: str
    ser_number: str
    capacity_device: Capacity_Device
    supply_id: int
    
@model_validator(mode="after")
def validate_bracket(self):
    if self.device_type == DeviceType.BRACKET and self.brand != Brand.MAXIM:
        raise ValueError("Бренд кронштейнов только Maxim")
    return self