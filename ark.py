_VERSION = 'dev'
_SUBVERSION = '25w09a'

from libs.olog import output as log
import libs.olog as olog


olog.logLevel = 5
log(f'Starting ArkLauncher Core, version {_VERSION}-{_SUBVERSION}.', type=olog.Type.INFO)