from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from models import Devices, Supply
from schema.supply_models import Supply as SupplySchema
from service.cache_service import CacheServiceSupply



class SupplyService:
    def __init__(self, session: Session, supply_cache: CacheServiceSupply):
        self.session = session
        self.supply_cache = supply_cache

    def get_supplies(self) -> list[SupplySchema]:
        cached = self.supply_cache.get_supplies()
        if cached is not None:
            return cached
        supplies = self.session.scalars(select(Supply)).all()
        result = [SupplySchema.model_validate(s) for s in supplies]
        self.supply_cache.set_supplies(result)
        return result

    def get_supply(self, supply_id: int):
        supply = self.session.get(Supply, supply_id)
        if supply is None:
            return None
        registered = self.session.scalar(
            select(func.count()).select_from(Devices).where(Devices.supply_id == supply_id)
        )
        return {
            "supply": SupplySchema.model_validate(supply),
            "total_price": supply.quantity * supply.unit_price,
            "ordered": supply.quantity,
            "registered": registered,
            "remaining": supply.quantity - registered,
        }

    def create_supply(self, supply: Supply) -> Supply:
        self.session.add(supply)
        self.session.commit()
        self.session.refresh(supply)
        return supply

    def delete_supply(self, supply_id: int) -> bool:
        result = self.session.execute(delete(Supply).where(Supply.id == supply_id))
        if supply_id is None:
            ValueError(status_code=404, detail= "Поставки с таким id не найдено")
        self.session.commit()
        return result.rowcount > 0