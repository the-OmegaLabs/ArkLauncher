import gui

from libs.olog import output as log
from libs.olog import WARN, ERROR, INFO, DEBUG

gui._VERSION = 'dev'
gui._SUBVERSION = '25w08e'

log(f'Starting ATCraft ArkLaucher, version {gui._VERSION}-{gui._SUBVERSION}.')
gui.main()