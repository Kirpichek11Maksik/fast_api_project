from handlers.supply import router as supply_router
from handlers.device import router as device_router
from handlers.users import router as users_router
routers = [supply_router, device_router, users_router]