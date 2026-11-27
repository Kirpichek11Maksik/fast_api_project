from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from models import Devices
from schema.device_models import DeviceSchema, DeviceCreateSchema
from depency import get_device_service, get_request_user_id
from service.device_service import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/get_devices/", response_model=list[DeviceSchema])
def get_devices(device_repo: Annotated[DeviceService, Depends(get_device_service)],):
    devices = device_repo.get_devices()
    if devices is None:
        raise HTTPException(status_code=404, detail="Девайсы отсутствуют")
    return devices


@router.get("/get_device/{ser_num}", response_model=DeviceSchema)
def get_device(ser_num: str, device_repo: Annotated[DeviceService, Depends(get_device_service)]):
    device = device_repo.get_device(ser_num)
    if device is None:
        raise HTTPException(status_code=404, detail="Девайс не найден")
    return device


@router.post("/add_device", response_model=DeviceSchema)
def create_device(
    device: DeviceCreateSchema,
    device_repo: Annotated[DeviceService, Depends(get_device_service)],
    user_id: int = Depends(get_request_user_id),
):
    zxc = Devices(**device.model_dump(), user_id=user_id)
    try:
        return device_repo.create_device(zxc)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/rename_local_device", response_model=DeviceSchema)
def local_rename(
    ser_number: str,
    location: str,
    device_service: Annotated[DeviceService, Depends(get_device_service)],
    user_id: int = Depends(get_request_user_id)
):
    return device_service.location_device_rename(ser_number, location), {"Локация девайса изменена"}


@router.delete("/delete_device/{ser_number}")
def drop_device(ser_number: str, device_repo: Annotated[DeviceService, Depends(get_device_service)],
                      user_id: int = Depends(get_request_user_id)
                      ):
    if not device_repo.delete_device(ser_number):
        raise HTTPException(status_code=404, detail="Устройство с таким серийным номером не найдено")
    return {"msg": "Удаление успешно"}