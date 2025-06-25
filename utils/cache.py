# utils/cache.py
class SimpleCache:
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

    def clear(self):
        self.cache.clear()

# Singleton instance
cache = SimpleCache()