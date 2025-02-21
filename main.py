import os

import darkdetect

import gui

from libs.olog import output as log
from libs.olog import WARN, ERROR, INFO, DEBUG

gui._VERSION = 'dev'
gui._SUBVERSION = '25w08e'

if os.path.exists('ark.conf'):
    with open('ark.conf', 'r') as f:
        for line in f.readlines():
            if line.startswith('Theme'):
                if line.split('=')[1].strip() == 'Auto':
                    gui._THEME = darkdetect.theme()
                else:
                    gui._THEME = line.split('=')[1].strip()

log(f'Starting ATCraft ArkLaucher, version {gui._VERSION}-{gui._SUBVERSION}.')
gui.main()