from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from sqlalchemy import delete
from database.models import Supply
from repository.supply_repository import SupplyRepository, get_suplies_repository
from schema.supply_models import Supply as supply_models

router = APIRouter(prefix="/supply", tags=["supply"])

@router.get("/supplies")
def get_supplies(repo: SupplyRepository = Depends(get_suplies_repository)):
    return repo.get_supplies()

@router.get("/{supply_id}")
def get_supply(supply_id: int, repo: SupplyRepository = Depends(get_suplies_repository)):
    return repo.get_supply(supply_id)

@router.post("/add_supply", response_model=supply_models)
def create_supply(supply: supply_models, repo: SupplyRepository = Depends(get_suplies_repository)):
    zxc = Supply(**supply.model_dump())
    return repo.create_supply(zxc)

@router.delete("/delete_supply/{supply_id}")
def drop_supply(supply_id: int, repo: SupplyRepository = Depends(get_suplies_repository)):
    if not repo.delete_supply(supply_id):
        raise HTTPException(status_code=404, detail="id такой поставки не существует")
    return {"msg": "Удаление успешно"}