import datetime
import sys
import inspect

from colorama import Fore, Style, Back


class Type():
    INFO = f'{Back.BLUE} INFO {Back.RESET}'
    ERROR = f'{Back.RED}{Style.BRIGHT} FAIL {Back.RESET}{Fore.RED}'
    WARN = f'{Back.YELLOW} WARN {Back.RESET}{Fore.YELLOW}'
    DEBUG = f'{Back.MAGENTA} DEBG {Back.RESET}'

logLevel = 5

def output(value: str, end: str = "\n", type: str = Type.INFO):
    now = datetime.datetime.now()
    if type == Type.DEBUG and logLevel == 5:
        sys.stdout.write(f"{Back.GREEN} {now.strftime('%H:%M:%S')} {Back.CYAN} " + inspect.stack()[1].filename.replace('\\', '/').split('/')[-1][:-3] + f" {type} {value} {Style.RESET_ALL}")
    elif type == Type.ERROR and logLevel >= 4:
        sys.stdout.write(f"{Back.GREEN} {now.strftime('%H:%M:%S')} {Back.CYAN} " + inspect.stack()[1].filename.replace('\\', '/').split('/')[-1][:-3] + f" {type} {value} {Style.RESET_ALL}")
    elif type == Type.WARN and logLevel >= 3:
        sys.stdout.write(f"{Back.GREEN} {now.strftime('%H:%M:%S')} {Back.CYAN} " + inspect.stack()[1].filename.replace('\\', '/').split('/')[-1][:-3] + f" {type} {value} {Style.RESET_ALL}")
    elif type == Type.INFO and logLevel >= 1:
        sys.stdout.write(f"{Back.GREEN} {now.strftime('%H:%M:%S')} {Back.CYAN} " + inspect.stack()[1].filename.replace('\\', '/').split('/')[-1][:-3] + f" {type} {value} {Style.RESET_ALL}")
    else:
        pass            
    sys.stdout.write(f'{end}')
