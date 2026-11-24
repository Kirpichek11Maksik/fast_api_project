import json

from redis import Redis
from schema.supply_models import Supply as SupplySchema

class CacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_supply(self) -> list[SupplySchema]:
        with self.redis as redis:
            supply_json = redis.lrange("Supplies", 0, -1)
        return [SupplySchema.model_validate(json.loads(supply)) for supply in supply_json]

    def set_supplies(self, supplies: list[SupplySchema]):
        supply_json = [supply.json() for supply in supplies]
        with self.redis as redis:
            redis.lpush("Supplies:", *supply_json)