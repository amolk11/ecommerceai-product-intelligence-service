# app/dependencies/cache.py

from functools import lru_cache

from app.cache.redis_cache import RedisCache
from app.cache.redis_client import get_redis_client


@lru_cache
def get_cache() -> RedisCache:
    return RedisCache(client=get_redis_client())
