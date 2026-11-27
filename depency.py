from fastapi import Depends, HTTPException, Request, Security, security, status
import jwt
from sqlalchemy.orm import Session

from cache import get_redis_connection
from database.accessor import SessionLocal
from service.cache_service import CacheServiceSupply, CacheServiceDevice
from service.device_service import DeviceService
from service.supply_service import SupplyService
from service.user_service import UserService
from service.auth_service import SECRET_KEY, AuthService
from excepction import TokenHasExpired, TokenNoCorrect

def get_db():
    with SessionLocal() as session:
        yield session


def get_cache_service() -> CacheServiceSupply:
    return CacheServiceSupply(get_redis_connection())

def get_cache_device_service() -> DeviceService:
    return CacheServiceDevice(get_redis_connection())


def get_device_service(session: Session = Depends(get_db),device_cache: CacheServiceDevice = Depends(get_cache_device_service)) -> DeviceService:
      return DeviceService(session, device_cache)

def get_supplies_service(
    session: Session = Depends(get_db),
    supply_cache: CacheServiceSupply = Depends(get_cache_service),
) -> SupplyService:
    return SupplyService(session, supply_cache)


def get_user_service(session: Session = Depends(get_db)) -> UserService:
    return UserService(session)

def get_auth_service(
    user_service: UserService = Depends(get_user_service),
) -> AuthService:
    return AuthService(user_service)

reusable_oauth2 = security.HTTPBearer()

def get_request_user_id(
    token: security.HTTPAuthorizationCredentials = Depends(reusable_oauth2),
) -> int:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise TokenHasExpired
    except (jwt.PyJWTError, KeyError):
        raise TokenNoCorrect
    return payload["user_id"]