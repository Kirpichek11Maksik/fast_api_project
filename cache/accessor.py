import redis
from setting import Settings

settings = Settings()

redis_client = redis.Redis(
    host=settings.CACHE_HOST,
    port=settings.CACHE_PORT,
    db=settings.CACHE_DB,
)


def get_redis_connection() -> redis.Redis:
    return redis_client


def set_zxc_count():
    redis_client.set("zxc_count", 1)