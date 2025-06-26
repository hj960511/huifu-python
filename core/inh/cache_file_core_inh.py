# core/cache_file_core_inh.py

import os
import pickle
import time
from base.cache_base import CacheBase
from cfg import Config

CACHE_DIR = Config.RUNTIME_CACHE_DIR+"/data"

class FileCache(CacheBase):
    def __init__(self):
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    def _get_path(self, key):
        return os.path.join(CACHE_DIR, f"{key}.pkl")

    def get(self, key):
        path = self._get_path(key)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as f:
            data = pickle.load(f)
            if data["expire"] is None or data["expire"] > time.time():
                return data["value"]
            else:
                self.delete(key)
        return None

    def set(self, key, value, ttl=None):
        path = self._get_path(key)
        expire = time.time() + ttl if ttl else None
        with open(path, "wb") as f:
            pickle.dump({"value": value, "expire": expire}, f)

    def delete(self, key):
        path = self._get_path(key)
        if os.path.exists(path):
            os.remove(path)

    def exists(self, key):
        path = self._get_path(key)
        return os.path.exists(path)
