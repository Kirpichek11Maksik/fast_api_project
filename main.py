from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from excepction import AppException
from handlers import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})