import json
from schema.device_models import DeviceSchema
from schema.supply_models import Supply as SupplySchema
from redis import Redis
from pydantic import TypeAdapter

class CacheServiceSupply:
    KEY = "supplies"
    TTL = 60

    def __init__(self, redis: Redis):
        self.redis = redis
        self._adapter = TypeAdapter(list[SupplySchema])

    def get_supplies(self) -> list[SupplySchema] | None:
        raw = self.redis.get(self.KEY)
        if raw is None:
            return None
        return self._adapter.validate_json(raw)

    def set_supplies(self, supplies: list[SupplySchema]) -> None:
        self.redis.set(self.KEY, self._adapter.dump_json(supplies), ex=self.TTL)

    def invalidate(self) -> None:
        self.redis.delete(self.KEY)

class CacheServiceDevice:
    KEY = "devices"
    TTL = 60

    def __init__(self, redis: Redis):
        self.redis = redis
        self._adapter = TypeAdapter(list[DeviceSchema])

    def get_devices(self) -> list[DeviceSchema] | None:
        raw = self.redis.get(self.KEY)
        if raw is None:
            return None
        return self._adapter.validate_json(raw)

    def set_devices(self, devices: list[DeviceSchema]) -> None:
        self.redis.set(self.KEY, self._adapter.dump_json(devices), ex=self.TTL)

    def invalidate(self) -> None:
        self.redis.delete(self.KEY)