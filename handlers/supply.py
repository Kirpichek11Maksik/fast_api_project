from typing import Annotated

from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy import delete
from database.models import Supply
from schema.supply_models import Supply as supply_models
from repository.supply_repository import SupplyRepository
from depency import get_suplies_repository


router = APIRouter(prefix="/supply", tags=["supply"])

@router.get("/supplies")
async def get_supplies(supply_repo: Annotated[SupplyRepository, Depends(get_suplies_repository)]):
    return supply_repo.get_supplies()

@router.get("/{supply_id}")
async def get_supply(supply_id: int, supply_repo: Annotated[SupplyRepository, Depends(get_suplies_repository)]):
    return supply_repo.get_supply(supply_id)

@router.post("/add_supply", response_model=supply_models)
async def create_supply(supply: supply_models, supply_repo: Annotated[SupplyRepository, Depends(get_suplies_repository)]):
    zxc = Supply(**supply.model_dump())
    return supply_repo.create_supply(zxc)

@router.delete("/delete_supply/{supply_id}")
async def drop_supply(supply_id: int, supply_repo: Annotated[SupplyRepository, Depends(get_suplies_repository)]):
    if not supply_repo.delete_supply(supply_id):
        raise HTTPException(status_code=404, detail="id такой поставки не существует")
    return {"msg": "Удаление успешно"}