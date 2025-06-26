# core/cache_base.py

from abc import ABC, abstractmethod


class CacheBase(ABC):
    @abstractmethod
    def get(self, key):
        pass
    @abstractmethod
    def set(self, key, value, ttl=None):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def exists(self, key):
        pass
