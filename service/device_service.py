from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from excepction import DeviceNotFound
from models import Devices, Supply
from service.cache_service import CacheServiceDevice
from schema.device_models import DeviceSchema

class DeviceService:
    def __init__(self, session: Session, cach_device: CacheServiceDevice):
        self.session = session
        self.cached_device = cach_device


    def get_devices(self) -> list[DeviceSchema]:
        cached = self.cached_device.get_devices()
        if cached is not None:
            return cached
        devices = list(self.session.scalars(select(Devices)).all())
        result = [DeviceSchema.model_validate(d) for d in devices]
        self.cached_device.set_devices(result)
        return result

    def get_device(self, ser_num: str) -> Devices | None:
        return self.session.scalar(select(Devices).where(Devices.ser_number == ser_num))

    def create_device(self, device: Devices) -> Devices:
        supply = self.session.get(Supply, device.supply_id)
        if supply is None:
            raise ValueError("Поставка не найдена")
        if (supply.device_type, supply.brand) != (device.device_type, device.brand):
            raise ValueError("Тип или бренд не совпадает с поставкой")
        count = self.session.scalar(
            select(func.count()).select_from(Devices).where(Devices.supply_id == supply.id)
        )
        if count >= supply.quantity:
            raise ValueError("Все устройства этой поставки уже заведены")
        self.session.add(device)
        self.session.commit()
        return device
    
    def location_device_rename(self, ser_number: str, location: str) -> Devices:
        device = self.session.scalar(
            select(Devices).where(Devices.ser_number == ser_number)
            )
        if device is None:
            raise DeviceNotFound
        device.location = location
        self.session.commit()
        self.cached_device.invalidate()
        return device

    def delete_device(self, ser_num: str) -> bool:
        result = self.session.execute(delete(Devices).where(Devices.ser_number == ser_num))
        self.session.commit()
        return result.rowcount > 0