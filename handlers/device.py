from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy import delete
from database.models import Device
from schema.device_models import Device as device_models
from repository.device_repository import DeviceRepository, get_devices_repository

router = APIRouter(prefix="/device", tags=["device"])

@router.get("/devices")
def get_supplies(repo: DeviceRepository = Depends(get_devices_repository)):
    return repo.get_devices()

@router.get("/{device_ser_num}")
def get_supply(ser_num: str, repo: DeviceRepository = Depends(get_devices_repository)):
    return repo.get_device(ser_num)

@router.post("/add_device", response_model=device_models)
def create_supply(device: device_models, repo: DeviceRepository = Depends(get_devices_repository)):
    zxc = Device(**device.model_dump())
    return repo.create_device(zxc)

@router.delete("/delete_device/{ser_number}")
def drop_supply(ser_number: str, repo: DeviceRepository = Depends(get_devices_repository)):
    if not repo.delete_device(ser_number):
        raise HTTPException(status_code=404, detail="id такой поставки не существует")
    return {"msg": "Удаление успешно"}