from database.database import get_db_session
from repository.device_repository import DeviceRepository
from repository.supply_repository import SupplyRepository


def get_devices_repository() -> DeviceRepository:
    return DeviceRepository(get_db_session())


def get_suplies_repository() -> SupplyRepository:
    return SupplyRepository(get_db_session())