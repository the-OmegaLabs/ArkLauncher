# Copyright 2025 Omega Labs, ArkLauncher Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import functools

from PIL import Image


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
