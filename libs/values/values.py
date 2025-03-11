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


import base64

import PIL.Image
from PIL import ImageTk


class NotificationIcon:
    def __init__(self, type):
        self.type = type

    def getImagePath(self):
        if self.type == "info":
            return "src/icon/notification/info.png"
        elif self.type == "warning":
            return "src/icon/notification/warning.png"
        elif self.type == "error":
            return "src/icon/notification/error.png"
        else:
            return "src/icon/notification/info.png"

    def _getImageBytes(self):
        return open(self.getImagePath(), "rb").read()

    def _getPhotoImage(self, method: str = "bytes"):
        if method == "bytes":
            return ImageTk.PhotoImage(data=self._getImageBytes())
        elif method == "path":
            return ImageTk.PhotoImage(file=self.getImagePath())

    def _getImageSize(self):
        return self._getPhotoImage().width(), self._getPhotoImage().height()

    def _getResizedImage(self, size: tuple):
        with PIL.Image.open(self.getImagePath()) as img:
            img = img.resize((size[0], size[1]))
            return img

    def _getResizedImageTk(self, size: tuple):
        return ImageTk.PhotoImage(self._getResizedImage(size))

    def _getPILImage(self):
        return PIL.Image.open(self.getImagePath())

    def _getB64Image(self):
        return base64.b64encode(self._getImageBytes())
