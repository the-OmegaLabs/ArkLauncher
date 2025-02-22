import os

import darkdetect

import gui

from libs.olog import output as log
from libs.olog import WARN, ERROR, INFO, DEBUG

gui._VERSION = 'dev'
gui._SUBVERSION = '25w08f'

log(f'Starting ATNetwork ArkLaucher, version {gui._VERSION}-{gui._SUBVERSION}.')
gui.main()