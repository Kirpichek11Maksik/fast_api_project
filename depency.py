from fastapi import Depends
from sqlalchemy.orm import Session

from cache import get_redis_connection
from database.accessor import SessionLocal
from service.cache_service import CacheService
from service.device_service import DeviceService
from service.supply_service import SupplyService
from service.user_service import UserService
from service.auth_service import AuthService


def get_db():
    with SessionLocal() as session:
        yield session


def get_cache_service() -> CacheService:
    return CacheService(get_redis_connection())


def get_device_service(session: Session = Depends(get_db)) -> DeviceService:
    return DeviceService(session)


def get_supplies_service(
    session: Session = Depends(get_db),
    supply_cache: CacheService = Depends(get_cache_service),
) -> SupplyService:
    return SupplyService(session, supply_cache)


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)

def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)
