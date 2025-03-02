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


import getpass
import os

username = getpass.getuser()


def getAvatar():
    try:
        account_pictures_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\AccountPictures"

        image_files = []
        for filename in os.listdir(account_pictures_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_path = os.path.join(account_pictures_dir, filename)
                image_files.append((file_path, os.path.getmtime(file_path)))

        if image_files:
            return max(image_files, key=lambda x: x[1])[0]
        elif os.path.exists("C:\\ProgramData\\Microsoft\\User Account Pictures\\user.png"):
            return "C:\\ProgramData\\Microsoft\\User Account Pictures\\user.png"
        else:
            return "src/Contributors/Stevesuk0.jpg"
    
    except:
        return "src/Contributors/Stevesuk0.jpg"
