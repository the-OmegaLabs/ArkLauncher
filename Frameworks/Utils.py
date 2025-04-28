# Copyright 2025 Omega Labs, ArkLauncher Contributors.
# Report bugs and issues to https://github.com/the-OmegaLabs/ArkLauncher/issues
#
#    ___         __      __                           __
#    /   |  _____/ /__   / /   ____ ___  ______  _____/ /_  ___  _____
#   / /| | / ___/ //_/  / /   / __ `/ / / / __ \/ ___/ __ \/ _ \/ ___/
#  / ___ |/ /  / ,<    / /___/ /_/ / /_/ / / / / /__/ / / /  __/ /
# /_/  |_/_/  /_/|_|  /_____/\__,_/\__,_/_/ /_/\___/_/ /_/\___/_/
#
# 　　　　　　／＞　　フ
# 　　　　　| 　_　 _ l
# 　 　　　／` ミ＿xノ
# 　　 　 /　　　 　 |
# 　　　 /　 ヽ　　 ﾉ
# 　 　 │　　|　|　|
# 　／￣|　　 |　|　|
# 　| (￣ヽ＿_ヽ_)__)
# 　＼二つ
#
#  ▲ this cat is called Ark
#
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
# The Dash Imaging Library (fork from PIL).
#
#
# License:
# This project is licensed under multiple licenses:
#
# Apache License 2.0: The new modifications and additions made by Omega Labs and ArkLauncher Contributors.
#
# Copyright (c) 2025 Omega Labs, ArkLauncher Contributors.
#
# Partial icensed under the Apache License, Version 2.0 (the "License");
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
#
# MIT License: Portions of the code derived from the original PIL (Python Imaging Library), created by Secret Labs AB and Fredrik Lundh.
#
# Copyright (c) 1997-2009 by Secret Labs AB.  All rights reserved.
# Copyright (c) 1995-2009 by Fredrik Lundh.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import maliang.toolbox
import socket
from PIL import Image, ImageDraw, ImageFilter, ImageGrab


def makeImageRadius(img, radius=30, alpha=0.5):
    img = img.convert("RGBA")

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, img.size[0], img.size[1]), radius, fill=int(256 * alpha))

    img.putalpha(mask)

    return img

def takeShot(x, y, w, h):
    img = ImageGrab.grab((x, y, x + w, y + h))
    return img


def makeImageBlur(img, radius=5):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def mergeImage(a: Image, b: Image):
    return Image.alpha_composite(a, b)

def makeImageMask(size, color=(0, 0, 0, 128), ):
    return Image.new("RGBA", size=size, color=color)

def loadFont(fontPath, FONT_LIST):
    if not fontPath in FONT_LIST:
        FONT_LIST.append(fontPath)
        maliang.toolbox.load_font(fontPath, private=True)  # must be private.

    return FONT_LIST

def testConnection():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except Exception as e:
        return False
    
def getRelFromAbs(x, y, root):
    return (x + root.winfo_x(), y + root.winfo_y())