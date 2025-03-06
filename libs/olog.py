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


import datetime
import inspect
import sys
import threading

from colorama import Fore, Style, Back, init

init()


class Type():
    INFO = f'{Back.BLUE} INFO {Back.RESET}'
    ERROR = f'{Back.RED}{Style.BRIGHT} FAIL {Back.RESET}{Fore.RED}'
    WARN = f'{Back.YELLOW} WARN {Back.RESET}{Fore.YELLOW}'
    DEBUG = f'{Back.MAGENTA} DEBG {Back.RESET}'


global logLevel
logLevel = 5


def output(value: str, end: str = "\n", type: str = Type.INFO):
    now = datetime.datetime.now()
    sys.stdout.write(f"{Back.GREEN} {now.strftime('%H:%M:%S')} {Back.CYAN} " +
                        inspect.stack()[1].filename.replace('\\', '/').split('/')[-1][
                        :-3] + f" {type} {value} {Style.RESET_ALL}")
    sys.stdout.write(f'{end}')
    sys.stdout.flush()


def outputa(value: str, end: str = "\n", type: str = Type.INFO):
    threading.Thread(target=_, args=(value, end, type)).start()