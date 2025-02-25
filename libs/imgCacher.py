from PIL import Image
import functools

class ImageLoader:
    _cache = {}

    @staticmethod
    @functools.lru_cache(maxsize=32)
    def X(path, size=None):
        key = (path, size)
        if key not in ImageLoader._cache:
            try:
                img = Image.open(path)
                if size:
                    img = img.resize(size, Image.Resampling.LANCZOS)
                ImageLoader._cache[key] = img
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                return None
        return ImageLoader._cache[key]

    @classmethod
    def C(cls):
        cls.X.cache_clear()
        cls._cache.clear()