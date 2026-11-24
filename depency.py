from fastapi import Depends

from database.database import get_db_session
from repository.device_repository import DeviceRepository
from repository.supply_repository import SupplyRepository
from repository.cache_repository import CacheRepository
from cache import get_redis_connection
from service.supply_service import SupplyService
def get_devices_repository() -> DeviceRepository:
    return DeviceRepository(get_db_session())


def get_suplies_repository() -> SupplyRepository:
    return SupplyRepository(get_db_session())

def get_cache_repository() ->CacheRepository:
    redis_connection = get_redis_connection()
    return CacheRepository(redis_connection)

def get_supplies_service(
    supply_repository: SupplyRepository = Depends(get_suplies_repository),
    supply_cache: CacheRepository = Depends(get_cache_repository),
) -> SupplyService:
    return SupplyService(
    supply_repository=supply_repository,
    supply_cache=supply_cache,
    )
