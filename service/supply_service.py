from dataclasses import dataclass

from schema.supply_models import Supply as SupplySchema
from repository import SupplyRepository, CacheRepository
from fastapi import Depends, FastAPI, APIRouter, HTTPException

@dataclass
class SupplyService:
    supply_repository: SupplyRepository
    supply_cache: CacheRepository

    def get_supplies(self):
        if supplies_cache := self.supply_cache.get_supply():
                return supplies_cache
        else:
            supplies = self.supply_repository.get_supplies()
            supplies_schema = [SupplySchema.model_validate(s) for s in supplies]
            self.supply_cache.set_supplies(supplies_schema)
            return supplies_schema