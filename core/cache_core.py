from flask import Flask

from core.inh.cache_file_core_inh import FileCache
from core.inh.cache_redis_core_inh import RedisCache


class CacheCore:
    def run(self, app: Flask):
        # 获取配置信息 并创建 本地缓存对象
        cache_type = app.config.get("CACHE_TYPE", "redis")
        if cache_type == "redis":
            print("✅ 当前缓存引擎：Redis")
            app.cc_local = RedisCache()
            pass
        elif cache_type == "file":
            print("✅ 当前缓存引擎：本地文件")
            app.cc_local = FileCache()
            pass
        else:
            raise ValueError(f"❌ 不支持的缓存类型: {cache_type}")


cc_local = CacheCore()