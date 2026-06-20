from abc import ABC, abstractmethod


class CacheManager(ABC):
    """
    Redis cache abstraction.
    """

    @abstractmethod
    def get(self, key: str):
        pass

    @abstractmethod
    def set(self, key: str, value, ttl: int):
        pass

    @abstractmethod
    def delete(self, key: str):
        pass
