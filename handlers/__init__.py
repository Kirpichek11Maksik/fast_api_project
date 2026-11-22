from websockets import Router

from handlers.supply import router as supply_router

routers = [supply_router]