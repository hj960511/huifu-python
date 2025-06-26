# core/cache_redis_core_inh.py
from base.cache_base import CacheBase
from core.redis_core import redis_client


class RedisCache(CacheBase):
    def __init__(self):
        self.client = redis_client.client  # 确保 redis_client 已初始化

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, ttl=None):
        if ttl:
            return self.client.setex(key, ttl, value)
        return self.client.set(key, value)

    def delete(self, key):
        return self.client.delete(key)

    def exists(self, key):
        return self.client.exists(key)
