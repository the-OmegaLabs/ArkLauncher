_VERSION = 'dev'
_SUBVERSION = '25w09a'

import libs.olog as olog
from libs.olog import output as log
import requests

from PIL import Image
from io import BytesIO


olog.logLevel = 5
log(f'Starting ArkLauncher Core, version {_VERSION}-{_SUBVERSION}.', type=olog.Type.INFO)


def getSourceContent(url):
    olog.output(f'Sending requests to {url}/metadata.json...')
    response = requests.get(f'{url}/metadata.json')
    metadata = response.json()
    log(f'Response from remote: {metadata}', type=olog.Type.DEBUG)
    
    log(f'Sending requests to: {url}/{metadata['icon']}', type=olog.Type.DEBUG)
    image = requests.get(f'{url}{metadata['icon']}')
    metadata['icon'] = Image.open(BytesIO(image.content))
    return (True, metadata)
