from colorama import Fore, Style, Back, init
import sys
import datetime



INFO = f'{Back.BLUE} INFO {Back.RESET}'
ERROR = f'{Back.RED}{Style.BRIGHT} FAIL {Back.RESET}{Fore.RED}'
WARN = f'{Back.YELLOW} WARN {Back.RESET}{Fore.YELLOW}'
DEBUG = f'{Back.MAGENTA} DEBG {Back.RESET}'

def output(*values: object, end: str = "\n", type: str = INFO):
    now = datetime.datetime.now()
    for i in values:
        sys.stdout.write(f'{Back.GREEN} {now.strftime("%H:%M:%S")} {type} {i} {Style.RESET_ALL}')

    sys.stdout.write(f'{end}')