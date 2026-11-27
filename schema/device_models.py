from pydantic import BaseModel, ConfigDict, Field, model_validator
from schema.supply_models import DeviceType, Brand


class Capacity_Device(BaseModel):
    human: int = Field(ge=300, le=3000)
    photo: int = Field(ge=300, le=3000)
    card: int = Field(ge=300, le=3000)
    event: int = Field(ge=150000, le=150000)


class DeviceCreateSchema(BaseModel):
    device_type: DeviceType
    brand: Brand
    location: str
    ip: str
    ser_number: str
    capacity_device: Capacity_Device
    supply_id: int
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_bracket(self):
        if self.device_type == DeviceType.BRACKET and self.brand != Brand.MAXIM:
            raise ValueError("Бренд кронштейнов только Maxim")
        return self


class DeviceSchema(DeviceCreateSchema):
    id: int
    user_id: int | None = None
    model_config = ConfigDict(from_attributes=True, extra="ignore")