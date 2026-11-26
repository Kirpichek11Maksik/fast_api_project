import json

from schema.supply_models import Supply as SupplySchema
from redis import Redis


class CacheService:
    def __init__(self, redis: Redis):
        self.redis = redis

    def get_supplies(self) -> list[SupplySchema] | None:
        raw = self.redis.get("supplies")
        if raw is None:
            return None
        return [SupplySchema.model_validate(item) for item in json.loads(raw)]

    def set_supplies(self, supplies: list[SupplySchema]):
        if not supplies:
            return
        pipe = self.redis.pipeline()
        pipe.delete("Supplies:")
        pipe.rpush("Supplies:", *(s.model_dump_json() for s in supplies))
        pipe.execute()