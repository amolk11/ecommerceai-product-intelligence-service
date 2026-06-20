import json
import redis
import time

from app.cache.cache_manager import CacheManager
from app.core.logger import get_logger

logger = get_logger(log_name="redis_cache", log_folder="cache")


class RedisCache(CacheManager):
    def __init__(self, client: redis.Redis):

        self.client = client

    def get(self, key: str):

        try:
            start = time.perf_counter()

            result = self.client.get(key)

            redis_time = time.perf_counter() - start
            logger.info("Redis GET took %.3fs", redis_time)

            if result is None:
                return None

            return json.loads(result)

        except (redis.RedisError, json.JSONDecodeError):
            logger.exception("Redis GET failed for key=%s", key)
            return None

    def set(self, key: str, value, ttl: int):
        try:
            serialized = json.dumps(value)
            self.client.set(name=key, value=serialized, ex=ttl)
        except redis.RedisError:
            logger.exception(f"Redis SET failed for key={key}")

    def ping(self) -> bool:
        try:
            return self.client.ping()
        except redis.RedisError:
            logger.exception("Redis ping failed")
            return False

    def delete(self, key):
        try:
            self.client.delete(key)
        except redis.RedisError:
            logger.exception("Redis DELETE failed for key=%s", key)
