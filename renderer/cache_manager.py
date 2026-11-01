import skia


class RenderCacheManager:

    def __init__(self):
        self._cache = {}

    def get(self, key: str) -> skia.Image:
        return self._cache.get(key)

    def set(self, key: str, img: skia.Image):
        self._cache[key] = img
