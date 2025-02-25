_VERSION = 'dev'
_SUBVERSION = '25w09a'

import libs.olog as olog
from libs.olog import output as log

olog.logLevel = 5
log(f'Starting ArkLauncher Core, version {_VERSION}-{_SUBVERSION}.', type=olog.Type.INFO)


def getSourceContent(url):
    olog.output(f'Sending requests to {url}...', type=olog.Type.DEBUG)
