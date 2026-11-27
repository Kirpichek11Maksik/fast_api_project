from typing import Annotated
from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy import delete
from models import Supply
from service.supply_service import SupplyService
from schema.supply_models import CreateSupplySchema
from depency import get_supplies_service, get_cache_service, get_supplies_service, get_request_user_id


router = APIRouter(prefix="/supply", tags=["supply"])

@router.get("/supplies")
async def get_supplies(supply_serv: Annotated[SupplyService, Depends(get_supplies_service)]):
    return supply_serv.get_supplies()

@router.get("/{supply_id}")
async def get_supply(supply_id: int, supply_repo: Annotated[SupplyService, Depends(get_supplies_service)]):
    return supply_repo.get_supply(supply_id)

@router.post("/create_supply", response_model=CreateSupplySchema)
async def create_supply(
    supply: CreateSupplySchema,
    supply_serv: Annotated[SupplyService, Depends(get_supplies_service)],
    user_id: int = Depends(get_request_user_id)
    ):
    zxc = Supply(**supply.model_dump())
    return supply_serv.create_supply(zxc)

@router.delete("/delete_supply/{supply_id}")
async def drop_supply(supply_id: int, supply_serv: Annotated[SupplyService, Depends(get_supplies_service)],
                      user_id: int = Depends(get_request_user_id)
                      ):
    if not supply_serv.delete_supply(supply_id):
        raise HTTPException(status_code=404, detail="id такой поставки не существует")
    return {"msg": "Удаление успешно"}