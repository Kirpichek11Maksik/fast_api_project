from datetime import date  
from decimal import Decimal
from enum import Enum
from pydantic import BaseModel, Field, model_validator


class DeviceType(str, Enum):
    TERMINAL = "terminal"
    ROUTER = "router"
    BRACKET = "bracket"


class Brand(str, Enum):
    HIKVISION = "Hikvision"
    MIKROTIK = "MikroTik"
    DAHUA = "Dahua"
    MAXIM = "Maxim"


class Supply(BaseModel):
    quantity: int
    device_type: DeviceType
    brand: Brand
    unit_price: Decimal
    supplier: str
    data_supply: date

    @model_validator(mode="after")
    def validate_bracket(self) -> "Supply":
        if self.device_type == DeviceType.BRACKET and self.brand != Brand.MAXIM:
            raise ValueError("Бренд кронштейнов только Maxim")
        return self

