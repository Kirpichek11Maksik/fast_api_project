from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from models import Devices
from schema.device_models import Device as device_models
from depency import get_device_service
from service.device_service import DeviceService

router = APIRouter(prefix="/device", tags=["device"])


@router.get("/devices")
async def get_devices(device_repo: Annotated[DeviceService, Depends(get_device_service)]):
    devices = device_repo.get_devices()
    if devices is None:
        raise HTTPException(status_code=404, detail="Девайсы отсутствуют")
    return devices


@router.get("/{ser_num}")
async def get_device(ser_num: str, device_repo: Annotated[DeviceService, Depends(get_device_service)]):
    device = device_repo.get_device(ser_num)
    if device is None:
        raise HTTPException(status_code=404, detail="Девайс не найден")
    return device


@router.post("/add_device", response_model=device_models)
def create_device(device: device_models,device_repo: Annotated[DeviceService, Depends(get_device_service)]):
    zxc = Devices(**device.model_dump())
    try:
        return device_repo.create_device(zxc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/delete_device/{ser_number}")
async def drop_device(ser_number: str, device_repo: Annotated[DeviceService, Depends(get_device_service)]):
    if not device_repo.delete_device(ser_number):
        raise HTTPException(status_code=404, detail="Устройство с таким серийным номером не найдено")
    return {"msg": "Удаление успешно"}