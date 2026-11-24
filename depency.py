from fastapi import Depends
from service.user import UserService
from database.accessor import get_db_session
from repository.device_repository import DeviceRepository
from repository.supply_repository import SupplyRepository
from repository.cache_repository import CacheRepository
from repository.user_repository import UserRepository
from cache import get_redis_connection
from sqlalchemy.orm import Session
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


def get_user_repository(db_session: Session = Depends(get_db_session)) -> UserRepository:
    return UserRepository(db_session=db_session)

def get_user_service(
      user_repository: UserRepository = Depends(get_user_repository)   
) -> UserService:
    return UserService(user_repository=user_repository)