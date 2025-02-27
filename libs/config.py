import getpass
import json
import os

config = {}
first = False

def _getConfigPath():
    #return os.path.join(os.path.expanduser(f'~/.config/arklauncher/'))
    return '.'


def _generateConfig(path):
    global first

    first = True
    os.makedirs(path, exist_ok=True)
    template = {
        'theme': 'system',
        'language': 'en',
        'border': 'smallround'
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