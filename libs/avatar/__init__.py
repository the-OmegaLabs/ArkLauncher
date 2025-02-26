import platform


if platform.system() == 'Windows':
    from libs.avatar.Windows import *

if platform.system() == 'Linux':
    from libs.avatar.Linux import *