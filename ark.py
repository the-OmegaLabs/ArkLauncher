# Copyright 2025 Omega Labs, ArkLauncher Contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

############################
from datetime import datetime
import time

import maliang.core.virtual
startLoadTime = time.time()
############################

import ctypes
import json
import math
import os
import platform
import socket
import threading
import traceback
import gc

import colorama
import darkdetect

import maliang
import maliang.animation
import maliang.color
import maliang.core
import maliang.standard
import maliang.theme
import maliang.toolbox

from PIL import (
    Image, 
    ImageDraw,
    ImageFilter,
    ImageGrab,
)

from Frameworks import Logger as olog
from Frameworks.Logger import output as log

import Frameworks.Configuration.config as configLib
import Frameworks.Tray as Tray

__version__ = 'dev'
__author__ = [ # Sorted by contributions 
    "Stevesuk0 (stevesukawa@outlook.com)",
    "bzym2 (mantouk@qq.com)",
    "HRGC-Sonrai",
    "PPicku"
]
_SUBVERSION = '25w12f'

# customized
try:
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    user32 = ctypes.windll.user32
    user32.SetWindowTextW(
        hwnd, f'ArkLauncher Console Interface - {__version__}, {_SUBVERSION}.')
except:
    pass


# config
WIDTH = 500
HEIGHT = 800

configLib.loadConfig()
config = configLib.config
locale = config['language']

images = {}
focus = False
ResPath = 'Resources'
_EMPTY = ('', '', '')
_FONTS = []
_THEME = config['theme']
_BORDER = config['border']
_SYSTEM = platform.system()
_SYSVER = platform.version()
_BACKGROUND = 'ChiesaBianca'
maliang.configs.Env.system = 'Windows10'
maliang.theme.manager.set_color_mode(_THEME)

if _SYSTEM == 'Windows':
    pass
elif _SYSTEM == 'Linux':
    pass

olog.logLevel = 5

log(f'Starting ArkLauncher GUI, version {__version__}-{_SUBVERSION}.')
log(f'Welcome to Ark!')
log(f'System: {_SYSTEM}, Version: {_SYSVER}.')

colorama.init()


def smooth_forward(t: float):
    return (1 - math.cos(t * math.pi)) / 2


def smooth_reverse(t: float):
    return (math.cos(t * math.pi) + 1) / 2

def getRelFromAbs(x, y):
    return (x - root.winfo_x(), y - root.winfo_y())


def takeShot(*args):
    x, y = root.winfo_x(), root.winfo_y()
    img = ImageGrab.grab((x, y, x + WIDTH, y + HEIGHT))
    return img


def focusWindow(*args):
    global focus
    if not focus:
        root.topmost(True)
        focus = True
        maliang.animation.MoveWindow(root, offset=(getRelFromAbs(root.winfo_screenwidth() - 515, root.winfo_y())), duration=500,
                                     controller=maliang.animation.controllers.ease_out, fps=1000).start()

    # maliang.animation.Animation(duration=100, command=root.alpha, controller=smooth_forward, end=_focus, fps=1000).start()


def minimizeWindow():
    global focus
    if focus:
        focus = False
        maliang.animation.MoveWindow(root, offset=getRelFromAbs(root.winfo_screenwidth(
        ) - 15, root.winfo_y()), duration=500, controller=maliang.animation.controllers.ease_out, fps=1000).start()
    # maliang.animation.Animation(duration=100, command=root.alpha, controller=smooth_reverse, fps=1000).start()


def minimizeAndExit():
    icon.stop()
    animation = maliang.animation.MoveWindow(root, offset=(
        600, 0), duration=500, controller=maliang.animation.controllers.ease_out, fps=1000)
    animation.end = lambda: (animation.stop(), root.destroy())
    animation.start()


def testDragAndDrop(*args):
    log(f'dnd: {args}')


def makeImageRadius(img, radius=30, alpha=0.5):
    img = img.convert("RGBA")

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, img.size[0], img.size[1]), radius, fill=int(256 * alpha))

    img.putalpha(mask)

    return img


def makeImageBlur(img, radius=5):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def makeImageMask(size, color=(0, 0, 0, 128), ):
    return Image.new("RGBA", size=size, color=color)


def mergeImage(a: Image, b: Image):
    try:
        return Image.alpha_composite(a, b)
    except ValueError:
        log(f'Can\'t merge image {a} and {b}.', type=olog.Type.ERROR)


def loadFont(fontPath):
    global _FONTS
    if not fontPath in _FONTS:
        _FONTS.append(fontPath)
        maliang.toolbox.load_font(fontPath, private=True)  # must be private.


def testConnection():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except Exception as e:
        return False


def updateFont():
    global FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT

    for i in os.listdir(f'{ResPath}/font'):
        loadFont(f'{ResPath}/font/{i}')

    log(f'Loaded {len(os.listdir(f'{ResPath}/font'))} fonts.')

    if locale == 'en':
        FONT_FAMILY = 'Segoe UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
    elif locale == 'ug':
        FONT_FAMILY = 'Segoe UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
    elif locale == 'tw':
        FONT_FAMILY = 'Microsoft Jhenghei'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
    elif locale == 'cnol':
        FONT_FAMILY = 'Meiryo UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY}'
    elif locale == 'jp':
        FONT_FAMILY = 'Yu Gothic UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Semilight'
    elif locale == 'cn':
    #     FONT_FAMILY = '源流黑体 CJK'
    #     FONT_FAMILY_BOLD = f'{FONT_FAMILY}'
        # FONT_FAMILY_LIGHT = f'{FONT_FAMILY}'
        FONT_FAMILY = 'Segoe UI'
        FONT_FAMILY_BOLD = f'源流黑体 CJK'
        FONT_FAMILY_LIGHT = f'源流黑体 CJK'
    """
        if locale == 'jp':
        FONT_FAMILY       = f'Yu Gothic UI'
        FONT_FAMILY_BOLD  = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
    elif locale in ('cn'):
    FONT_FAMILY       = f'Noto Sans'
    FONT_FAMILY_BOLD  = f'{FONT_FAMILY} Bold'
    FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
    elif locale in ('sb'):
        FONT_FAMILY       = f'Simsun'
        FONT_FAMILY_BOLD  = f'Simhei'
        FONT_FAMILY_LIGHT = f'FangSong'
    elif locale in ('ko'):
        FONT_FAMILY       = f'Malgun Gothic'
        FONT_FAMILY_BOLD  = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'Malgun Gothic'
    elif locale in ('en'):
        FONT_FAMILY       = f'Segoe UI'
        FONT_FAMILY_BOLD  = f'Segoe UI Semibold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'"""

    log(f'Changed font to {FONT_FAMILY} (Bold: {FONT_FAMILY_BOLD}, Light: {FONT_FAMILY_LIGHT}).')


def refreshImage(*args, threaded: bool):
    global images

    del images

    def loadImage(path):
        try:
            img = Image.open(path)
            return img
        except Exception as e:
            tracebackWindow(e)
            return None

    def threadedImageOpen(path, dict_key, category=None):
        img = loadImage(path)
        if img:
            if category:
                if category not in images:
                    images[category] = {}
                images[category][dict_key] = img
            else:
                images[dict_key] = img
            # log(f"Loaded image: {path}")

    theme = darkdetect.theme().lower() if _THEME == 'system' else _THEME

    # Initialize images dictionary with categories
    images = {
        'contributors': {},
        'country': {}
    }

    # Define image paths with categories
    image_paths = {
        'contributors': {
            'maliang':        f'{ResPath}/icon/contributors/maliang.png',
            'Stevesuk0':      f'{ResPath}/icon/contributors/Stevesuk0.png',
            'bzym2':          f'{ResPath}/icon/contributors/bzym2.png',
            'HRGC-Sonrai':    f'{ResPath}/icon/contributors/HRGC-Sonrai.png',
            'the-OmegaLabs':  f'{ResPath}/icon/contributors/the-OmegaLabs.png',
        },
        'country': {
            'cn':             f'{ResPath}/icon/both/country_cn.png',
            'jp':             f'{ResPath}/icon/both/country_jp.png',
            'ko':             f'{ResPath}/icon/both/country_ko.png',
            'en':             f'{ResPath}/icon/both/country_us.png',
            'sb':             f'{ResPath}/icon/both/transgender.png',
            'ug':             f'{ResPath}/icon/both/country_cn.png',
            'tw':             f'{ResPath}/icon/both/country_cn.png',
            'cnol':           f'{ResPath}/icon/both/country_ching.png'
        },
        'background': {
            'ChiesaBianca':   f'{ResPath}/icon/background/ChiesaBianca.png',
            'Concept':              f'{ResPath}/icon/background/g.png'
        },
        None: {  # Regular images without category
            'icon_quick':     f'{ResPath}/icon/both/quick.png',
            'icon_unknown':   f'{ResPath}/icon/both/unknown.png',
            'icon_logo':      f'{ResPath}/icon/main.png',
            'icon_exit':      f'{ResPath}/icon/{theme}/exit.png',
            'icon_minimize':  f'{ResPath}/icon/{theme}/minimize.png',
            'icon_return':    f'{ResPath}/icon/{theme}/return.png',
            'icon_settings':  f'{ResPath}/icon/{theme}/settings.png',
            'icon_about':     f'{ResPath}/icon/{theme}/about.png',
            'icon_language':  f'{ResPath}/icon/{theme}/language.png',
            'icon_network':   f'{ResPath}/icon/{theme}/network.png',
            'icon_account':   f'{ResPath}/icon/{theme}/account.png',
            'icon_customize': f'{ResPath}/icon/{theme}/customize.png',
            'icon_dark':      f'{ResPath}/icon/{theme}/dark.png',
            'icon_light':     f'{ResPath}/icon/{theme}/light.png',
            'icon_auto':      f'{ResPath}/icon/{theme}/auto.png',
            'icon_info':      f'{ResPath}/icon/{theme}/info.png',
            'icon_round':     f'{ResPath}/icon/{theme}/round.png',
            'icon_square':    f'{ResPath}/icon/{theme}/square.png',
            'icon_search':    f'{ResPath}/icon/{theme}/search.png',
            'icon_launch':    f'{ResPath}/icon/{theme}/launch.png',
            'icon_close':     f'{ResPath}/icon/{theme}/close.png'
        }
    }

    # Load all images with their respective categories
    for category, items in image_paths.items():
        for key, path in items.items():
            if threaded:
                threading.Thread(target=threadedImageOpen,
                                 args=(path, key, category)).start()
            else:
                threadedImageOpen(path, key, category)

    log(f'Loaded {len(image_paths['contributors']) + len(image_paths["country"]) + len(image_paths[None])} images.')


def getImage(target, category=None):
    try:
        if category:
            img = images[category][target]
        else:
            img = images[target]

        return img
    except:
        log(f'Image \"{target}\" is missing from category \"{category}\".',
            type=olog.Type.WARN)
        return images['icon_unknown']


def openGithub(name):
    os.system(f'start https://github.com/{name}')


def createRoot(x=710, y=200):
    global root

    root = maliang.Tk(size=(WIDTH, HEIGHT), position=(100000, 100000))
    root.geometry(size=(WIDTH, HEIGHT), position=(
        root.winfo_screenwidth() - 15, root.winfo_screenheight() - 880))
    root.title(f'{translate("prodname")} {translate(__version__)}-{_SUBVERSION}')
    root.overrideredirect(True)
    root.minsize(WIDTH, HEIGHT)
    root.maxsize(WIDTH, HEIGHT)
    root.alpha(0.95)
    maliang.theme.manager.customize_window(
        root, disable_maximize_button=True, border_type=_BORDER)
    maliang.theme.manager.apply_file_dnd(window=root, command=testDragAndDrop)


def createPage():
    global root

    cv = maliang.Canvas(root, auto_zoom=False)
    cv.place(width=WIDTH, height=HEIGHT - 65, x=0, y=65)

    root.icon(maliang.PhotoImage(getImage('icon_logo').resize((32, 32), 1)))
    return cv

def createTopBar():
    global topBar, topImage, topMask, backgroundImage, topMinimizeMask, topExitMask, topIconMask, logo

    backgroundImage     = getImage(_BACKGROUND, 'background')

    topBar = maliang.Canvas(root, auto_zoom=False)
    topBar.place(width=WIDTH, height=65, x=0, y=0)

    topImage            = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(makeImageBlur(backgroundImage.crop((0, 0, WIDTH, 65)), radius=10)))
    topMask             = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(makeImageMask(size=(WIDTH, 65))))
    topMinimizeMask     = maliang.Image(topMask, position=(int(WIDTH - (65 * 2)), 0), image=maliang.PhotoImage(makeImageMask((65, 65), color=(0, 0, 0, 80))))
    topExitMask         = maliang.Image(topMask, position=(int(WIDTH - (65 * 1)), 0), image=maliang.PhotoImage(makeImageMask((65, 65), color=(120, 0, 0, 128))))
    topIconMask         = maliang.Image(topMask, position=(0, 0),image=maliang.PhotoImage(makeImageMask(size=(65, 65), color=(0, 0, 0, 16))))
    logo                = maliang.IconButton(topIconMask, size=(65, 65), position=(305, 2), image=maliang.PhotoImage(getImage('icon_logo').resize((40, 40), 1)))
    minimize            = maliang.IconButton(topMinimizeMask, (2, 2), (61, 61), image=maliang.PhotoImage(getImage('icon_minimize').resize((40, 40), 1)), command=minimizeWindow)
    exit                = maliang.IconButton(topExitMask, (2, 2), (61, 61), image=maliang.PhotoImage(getImage('icon_exit').resize((60, 60), 1)), command=minimizeAndExit)
    

    logo.style.set(bg=_EMPTY, ol=_EMPTY)
    #exit.style.set(bg=('', '#990000', ''), ol=('', '#EEEEEE'))
    exit.style.set(bg=('', '#990000', ''), ol=('', '#990000', '#990000'))
    minimize.style.set(bg=('', '', ''), ol=(''))
    #minimize.style.set(bg=('', '', ''), ol=('', ''))
    logo.style.set(bg=_EMPTY, ol=_EMPTY)

    
    root.bind("<ButtonPress-1>", focusWindow)


close = None

def updateTopBar(barType):
    global topMask, topImage, topSearchMask, topMask, logo, close
    upHEIGHT            = 65
    if barType == 'mainPage':
        if close:
            maliang.animation.MoveWidget(close, duration=350, fps=1000, offset=(0, -65), controller=maliang.animation.ease_out).start()
        #topImage            = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(makeImageBlur(backgroundImage.crop((0, 0, WIDTH, upHEIGHT)), radius=10)))
        #topMask             = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(makeImageMask(size=(WIDTH, upHEIGHT))))
        topSearchMask       = maliang.Image(topMask, position=(upHEIGHT, -65), image=maliang.PhotoImage(makeImageMask(size=(int(WIDTH - (upHEIGHT * 3)), upHEIGHT), color=(0, 0, 0, 50))))
        searchBox           = maliang.InputBox(topSearchMask, position=(0, 2), size=(int(WIDTH - (upHEIGHT * 3)), upHEIGHT - 4), placeholder=translate('search'), family=FONT_FAMILY_BOLD, fontsize=18)
        searchBox.style.set(bg=_EMPTY, ol=_EMPTY)



        maliang.animation.MoveWidget(logo, duration=350, fps=1000, offset=(-305, 0), controller=maliang.animation.ease_out).start(delay=25)
        maliang.animation.MoveWidget(topSearchMask, duration=350, fps=1000, offset=(0, 65), controller=maliang.animation.ease_out).start(delay=25)

    elif barType == 'welcomePage':
        pass
        
    else:
        def switchIn():
            nonlocal avatar
            avatar             = maliang.IconButton(topMask, size=(63, 63), position=(int(WIDTH - (65 * 4)), 3), image=maliang.PhotoImage(makeImageRadius(getImage('icon_account'), 128, 0.7).resize((40, 40), 1)))
            avatar.style.set(bg=_EMPTY, ol=_EMPTY)

        if topSearchMask:
            maliang.animation.MoveWidget(topSearchMask, duration=350, fps=1000, offset=(0, -65), controller=maliang.animation.ease_out).start(delay=25)
        upHEIGHT            = 65

        now = datetime.now()
        curTimeMonth        = maliang.Text(topMask, position=(85, 14), text=f'{now.strftime("%Y/%m/%d")}', family=FONT_FAMILY, fontsize=10)
        curTimeDay          = maliang.Text(topMask, position=(85, 23), text=f'{now.strftime("%H:%M")}', family=FONT_FAMILY_BOLD, fontsize=23)
        
        avatar = None

        curTimeMonth.style.set(fg='#A5A9AC')


        maliang.animation.MoveWidget(logo, duration=350, fps=1000, offset=(305, 0), controller=maliang.animation.ease_out).start(delay=25)
        close = maliang.IconButton(topIconMask, (2, -63), (upHEIGHT - 4, upHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_close').resize((40, 40), 1)), command=lambda: (curTimeMonth.destroy(), curTimeDay.destroy(), avatar.destroy(), changeWindow(mainPage)))
        close.style.set(bg=('', '', ''), ol=(''))  
        maliang.animation.MoveWidget(close, duration=350, fps=1000, offset=(0, 65), controller=maliang.animation.ease_out).start(delay=25)

        cv.after(100, switchIn)

def changeWindow(window):
    def destroy(widget: maliang.Canvas, sleep):
        time.sleep(sleep)
        widget.destroy()
        gc.collect()

    log(f'Perform change canvas to "{window.__name__}"...',
        type=olog.Type.INFO)
    threading.Thread(target=destroy, args=(cv, 1)).start()
    try:
        updateTopBar(window.__name__)
        window()
    except RuntimeError:
        log('Calling Tcl from tray thread.', type=olog.Type.WARN)


def loadLocale():
    global lang_dict

    lang_dict = {}

    for i in os.listdir(f'{ResPath}/lang'):
        if i.endswith('.json'):
            with open(f'{ResPath}/lang/{i}', encoding='utf-8') as f:
                lang_dict[i[:-5]] = json.loads(f.read())

    log(f'Loaded {len(os.listdir(f'{ResPath}/lang'))} locales.')


def translate(target):
    try:
        text = lang_dict[locale][target]
        return text
    except:
        log(f'String \"{target}\" missing in language \"{locale}\".',
            type=olog.Type.WARN)
        return target


def welcomePage():
    global locale, cv
    cv = createPage()

    backgroundImage = mergeImage(makeImageBlur(getImage(_BACKGROUND, 'background'), radius=25),
                                 makeImageMask((500, 800), (0, 0, 0, 64)))

    background = maliang.Image(cv, position=(0, 0), size=(500, 800), image=maliang.PhotoImage(backgroundImage))
    

    FONT_FAMILY_BOLD = 'Microsoft YaHei UI Bold'

    maliang.Image(cv, (40, 75), image=maliang.PhotoImage(
        getImage('icon_logo').resize((150, 150), 1)))
    text_welcome = maliang.Text(
        cv, (55, 250), family=FONT_FAMILY_BOLD, fontsize=30)
    text_desc = maliang.Text(
        cv, (55, 300), family=FONT_FAMILY_BOLD, fontsize=17)
    text_license = maliang.Text(
        cv, (85, 555), family=FONT_FAMILY_BOLD, fontsize=15)
    text_collect = maliang.Text(
        cv, (85, 593), family=FONT_FAMILY_BOLD, fontsize=15)
    text_button_chinese = maliang.Text(
        cv, (210, 659), text="中文", fontsize=17, family=FONT_FAMILY_BOLD)
    maliang.Text(cv, (330, 659), text="English",
                 fontsize=17, family=FONT_FAMILY_BOLD)
    button = maliang.Button(cv, (50, 650), size=(100, 40), command=lambda: (updateFont(), changeWindow(mainPage)), fontsize=16,
                            family=FONT_FAMILY_BOLD)
    button.disable(True)

    def agreeLicense(enable):
        button.disable(not enable)

    def changeLanguage(lang_key):
        global locale
        locale = lang_key

        text_welcome.set(translate('welcome'))
        text_desc.set(translate('desc'))
        text_license.set(translate('license'))
        text_collect.set(translate('collect'))
        text_button_chinese.set(translate('lang_chinese'))
        button.set(translate('button'))

        configLib.setConfig('language', locale)
        configLib.sync()

    def changeToEnglish(_):
        changeLanguage('en')

    def changeToChinese(_):
        changeLanguage('cn')

    maliang.CheckBox(cv, (50, 550), command=agreeLicense,
                     default=False, length=23)
    maliang.CheckBox(cv, (50, 590), default=True, length=23)
    langEN = maliang.RadioBox(
        cv, (290, 655), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(
        cv, (170, 655), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)


    changeLanguage('cn')

    root.mainloop()


def aboutPage():
    pass


def mainPage():
    global cv
    cv = createPage()
    cv.bind("<Escape>", lambda event: minimizeAndExit())

    _DRAG = [0, 0]

    def Drag(event):
        nonlocal _DRAG
        _DRAG[0] = event.x
        _DRAG[1] = event.y

    def moveWindow(event):
        dx = event.x - _DRAG[0]
        dy = event.y - _DRAG[1]

        root.geometry(position=(root.winfo_x() + dx, root.winfo_y() + dy))

    backgroundImage = getImage(_BACKGROUND, 'background').crop((0, 65, WIDTH, HEIGHT))

    background = maliang.Image(cv, position=(0, 0), size=(
        WIDTH, HEIGHT), image=maliang.PhotoImage(backgroundImage))

    bottomHEIGHT        = 265
    bottomMaskHEIGHT    = 70
    bottomLMaskHEIGHT   = 130
    bottomImage         = maliang.Image(cv, position=(0, 535), image=maliang.PhotoImage(makeImageBlur(backgroundImage.crop((0, HEIGHT - bottomHEIGHT, WIDTH, HEIGHT)), radius=10)))
    bottomMask          = maliang.Image(cv, position=(0, 535), image=maliang.PhotoImage(makeImageMask(size=(HEIGHT, bottomHEIGHT))))
    bottomSettingsMask  = maliang.Image(bottomMask, position=(bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=maliang.PhotoImage(makeImageRadius(makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
    bottomAccountMask   = maliang.Image(bottomMask, position=(500 - bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=maliang.PhotoImage(makeImageRadius(makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
    bottomSubMask       = maliang.Image(bottomMask, position=(0, bottomMaskHEIGHT), image=maliang.PhotoImage(makeImageMask((WIDTH, bottomLMaskHEIGHT), color=(0, 0, 0, 64))))
    bottomLaunchMask    = maliang.Image(bottomSubMask, position=(10, 7), image=maliang.PhotoImage(makeImageMask((480, 116), color=(0, 0, 0, 64))))

    settings            = maliang.IconButton(bottomSettingsMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_settings').resize((40, 40), 1)), command=lambda: (changeWindow(settingsPage)), anchor='center')
    account             = maliang.IconButton(bottomAccountMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_account').resize((40, 40), 1)), command=lambda: changeWindow(settingsAccountPage), anchor='center')

    launch              = maliang.Button(bottomLaunchMask, (0, 0), size=(480, 116))
    launchIcon          = maliang.Image(launch, (bottomLMaskHEIGHT // 2 - 5, bottomLMaskHEIGHT // 2 - 7),image=maliang.PhotoImage(getImage('icon_launch').resize((80, 80), 1)), anchor='center')
    launchDesc          = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 35), text='启动游戏', family=FONT_FAMILY,fontsize=17)
    launchTitle         = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 10), text='Meira Client', family=FONT_FAMILY_BOLD, fontsize=25)

    launch.style.set(fg=('', '', ''), bg=('', '', ''), ol=('#4C4849', '#BBBBBB'))
    account.style.set(bg=_EMPTY, ol=_EMPTY)
    settings.style.set(bg=_EMPTY, ol=_EMPTY)

    # logo.bind("<B1-Motion>", on_drag_motion)

    root.mainloop()


def settingsPage():
    global cv
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(mainPage))


    backgroundImage = mergeImage(makeImageBlur(getImage(_BACKGROUND, 'background'), radius=25),
                                 makeImageMask((500, 800), (0, 0, 0, 64)))

    background = maliang.Image(cv, position=(0, 0), size=(500, 800), image=maliang.PhotoImage(backgroundImage))
    
    optionsImage         = maliang.Image(cv, position=(0, 0), size=(500, 50), image=maliang.PhotoImage(makeImageBlur(backgroundImage.crop((0, 0, 500, 50)))))
    optionsMask          = maliang.Image(cv, position=(0, 0), size=(500, 50), image=maliang.PhotoImage(makeImageMask(size=(500, 50), color=(0, 0, 0, 80))))
    

    options = maliang.SegmentedButton(optionsMask, position=(250, 25), family=FONT_FAMILY_BOLD, fontsize=16, anchor='center', default=0, text=[translate('account'), translate('locale'), translate('network'), translate('customize'), translate('about')])
    options.style.set(bg=('', ''), ol=('', ''))
    for i in options.children:
        i.style.set(fg=('#888888', '#AAAAAA', '#CCCCCC', '#FFFFFF'), bg=('', '', '', '', '', ''), ol=('', '', '', '', '', ''))

    root.mainloop()


def settingsAccountPage():
    global cv

    cv = createPage()


def settingsNetworkPage():
    pass


def settingsCustomizePage():
    pass


def settingsLanguagePage():
    pass


def tracebackWindow(exception: Exception):
    log('Starting Traceback window because a exception detected.', type=olog.Type.WARN)

    tracelist = ''.join(traceback.format_exception(exception)).split('\n')

    for i in tracelist[:-1]:
        log(i, type=olog.Type.ERROR)

    width = 1000
    height = len(tracelist[:-1]) * 20 + 200
    root = maliang.Tk(size=(width, height),
                      title=f'ArkLauncher traceback window | {__version__}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=width, height=height)

    text_title = maliang.Text(cv, (50, 50), fontsize=23)
    text_title.set('An error detected.')

    text_title = maliang.Text(cv, (50, 80), fontsize=17)
    text_title.set(
        'You can take an screenshot in this window, and send it to the author.')

    text_trace = maliang.Text(cv, (50, 130), fontsize=14)
    text_trace.set(str(''.join(traceback.format_exception(exception))))

    root.at_exit(exit)
    root.bind('<Escape>', exit)
    root.center()
    root.mainloop()


try:
    refreshImage(threaded=False)

    hidden_menu = (
        Tray.MenuItem('Focus', focusWindow, default=True),
        Tray.Menu.SEPARATOR,
        Tray.MenuItem('Exit', minimizeAndExit)
    )

    icon = Tray.Icon("name", getImage('icon_logo'),
                        "ArkLauncher Tray", menu=hidden_menu)

    threading.Thread(target=icon.run, daemon=True).start()

    loadLocale()
    updateFont()  # auto select font

    createRoot()
    createTopBar()
    
    focusWindow()

    log(f'Loaded ArkLauncher in {int((time.time() - startLoadTime) * 1000)}ms.')

    if configLib.first:
        threading.Thread(target=lambda: updateTopBar('welcomePage')).start()
        welcomePage()
    else:
        threading.Thread(target=lambda: updateTopBar('mainPage')).start()
        mainPage()

except Exception as f:
    tracebackWindow(f)
