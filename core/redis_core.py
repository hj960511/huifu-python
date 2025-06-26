# core/redis.py
import redis

from flask import current_app, Flask
from functools import wraps


class RedisClient:
    def __init__(self):
        self.redis_client = None

    def run(self, app: Flask):
        """初始化 Redis 客户端"""
        config = app.config.get('REDIS_CONFIG', {})
        pool = redis.ConnectionPool(
            host=config.get('CACHE_REDIS_HOST', 'localhost'),
            port=config.get('CACHE_REDIS_PORT', 6379),
            password=config.get('CACHE_REDIS_PASSWORD'),
            db=config.get('CACHE_REDIS_DB', 0),
            decode_responses=True  # 自动解码响应为字符串
        )
        self.redis_client = redis.Redis(connection_pool=pool)

        # 尝试连接 Redis
        try:
            self.redis_client.ping()
            print("✅ Redis 连接成功！")
        except Exception as e:
            print(f"❌ Redis 连接失败: {str(e)}")

    @property
    def client(self):
        """返回 Redis 客户端实例"""
        if self.redis_client is None:
            raise RuntimeError("Redis 未初始化，请先调用 init_app 方法")
        return self.redis_client

    def set(self, key, value, ttl=None):
        """设置键值对，支持过期时间"""
        if ttl:
            return self.client.setex(key, ttl, value)
        return self.client.set(key, value)

    def get(self, key):
        """获取键值"""
        return self.client.get(key)

    def delete(self, key):
        """删除键"""
        return self.client.delete(key)

    def exists(self, key):
        """检查键是否存在"""
        return self.client.exists(key)


# 全局 Redis 实例
redis_client = RedisClient()
