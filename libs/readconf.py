import getpass
import json
import os

username = getpass.getuser()


def getConfPath():
    return os.path.join(os.path.expanduser(f'~/.config/arklauncher/'))


def genConf():
    if not os.path.exists(getConfPath()):
        os.makedirs(getConfPath(), exist_ok=True)
        with open(os.path.join(getConfPath(), 'config.json'), 'w') as f:
            f.write('''{
                "avatar": "Auto",
                "language": "cn"
            }''')


def getConf():
    if not os.path.exists(getConfPath()):
        genConf()
    with open(os.path.join(getConfPath(), 'config.json'), 'r') as f:
        return json.load(f)


def getSubConf(classname):
    return getConf()[classname]
