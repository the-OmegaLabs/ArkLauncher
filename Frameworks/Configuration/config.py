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


import json
import os
import platform

config = {}
first = False


def _getConfigPath():
    # return os.path.join(os.path.expanduser(f'~/.config/arklauncher/'))
    return '.'


def _generateConfig(path):
    global first

    first = True
    os.makedirs(path, exist_ok=True)
    template = {
        'theme': 'system',
        'style': f'{platform.system()}{platform.release()}',
        'language': 'en',
        'border': 'smallround',
    }
    with open(f'{path}/config.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(template, ensure_ascii=False, indent=4))


def loadConfig():
    global config
    if not os.path.exists(f'{_getConfigPath()}/config.json'):
        _generateConfig(_getConfigPath())
    with open(f'{_getConfigPath()}/config.json', encoding='utf-8') as f:
        config.update(json.loads(f.read()))


def setConfig(key: str, value: object):
    config[key] = value


def sync():
    with open(f'{_getConfigPath()}/config.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(config, ensure_ascii=False, indent=4))
