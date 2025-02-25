from PIL import Image, ImageOps
import functools

class Loader:
    _cache = {}

    @staticmethod
    @functools.lru_cache(maxsize=32)
    def load_image(path, size=None):
        key = (path, size)
        if key not in Loader._cache:
            try:
                img = Image.open(path)
                if size:
                    img = img.resize(size, Image.Resampling.LANCZOS)
                Loader._cache[key] = img
            except Exception as e:
                print(f"Error loading image {path}: {e}")
                return None
        return Loader._cache[key]