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
import time
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

import colorama
import darkdetect

import maliang
import maliang.animation
import maliang.color
import maliang.core
import maliang.standard
import maliang.theme
import maliang.toolbox

from Frameworks.DashImaging import (
    Image, 
    ImageDraw,
    ImageFilter,
    ImageGrab,
    ImageTk,
)

from Frameworks import Logger as olog
from Frameworks.Logger import output as log

import Frameworks.Configuration.config as configLib
import Frameworks.LightTray as LightTray

# from libs.utils import systemDetector as sd


_VERSION = 'dev'
_SUBVERSION = '25w11f'

# customized
try:
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    user32 = ctypes.windll.user32
    user32.SetWindowTextW(
        hwnd, f'ArkLauncher Console Interface - {_VERSION}, {_SUBVERSION}.')
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
maliang.configs.Env.system = 'Windows10'
maliang.theme.manager.set_color_mode(_THEME)

if _SYSTEM == 'Windows':
    pass
elif _SYSTEM == 'Linux':
    pass

olog.logLevel = 5

log(f'Starting ArkLauncher GUI, version {_VERSION}-{_SUBVERSION}.')
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
        root.topmost(False)
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
        log(f'Loaded font \"{fontPath}\".')


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
    else:
        FONT_FAMILY = 'Microsoft YaHei UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
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
            'g':              f'{ResPath}/icon/background/g.png'
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
            'icon_launch':    f'{ResPath}/icon/{theme}/launch.png'
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
    root.title(f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')
    root.overrideredirect(True)
    root.minsize(WIDTH, HEIGHT)
    root.maxsize(WIDTH, HEIGHT)
    maliang.theme.manager.customize_window(
        root, disable_maximize_button=True, border_type=_BORDER)
    maliang.theme.manager.apply_file_dnd(window=root, command=testDragAndDrop)


def createPage():
    global root

    cv = maliang.Canvas(root, auto_zoom=True)
    cv.place(width=WIDTH, height=HEIGHT)

    root.icon(ImageTk.PhotoImage(getImage('icon_logo').resize((32, 32), 1)))
    return cv


def changeWindow(window):
    log(f'Perform change canvas to "{window.__name__}"...',
        type=olog.Type.INFO)
    # cv.destroy()
    try:
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

            log(f'Loaded locale file "{i}"...')


def translate(target):
    try:
        text = lang_dict[locale][target]
        return text
    except:
        log(f'String \"{target}\" missing in language \"{locale}\".',
            type=olog.Type.WARN)
        return target


def welcomePage():
    global locale
    cv = createPage()

    FONT_FAMILY_BOLD = 'Microsoft YaHei UI Bold'

    maliang.Image(cv, (50, 75), image=ImageTk.PhotoImage(
        getImage('icon_logo').resize((150, 150), 1)))
    text_welcome = maliang.Text(
        cv, (50, 250), family=FONT_FAMILY_BOLD, fontsize=30)
    text_desc = maliang.Text(
        cv, (50, 300), family=FONT_FAMILY_BOLD, fontsize=17)
    text_license = maliang.Text(
        cv, (85, 605), family=FONT_FAMILY_BOLD, fontsize=15)
    text_collect = maliang.Text(
        cv, (85, 643), family=FONT_FAMILY_BOLD, fontsize=15)
    text_button_chinese = maliang.Text(
        cv, (210, 709), text="中文", fontsize=17, family=FONT_FAMILY_BOLD)
    maliang.Text(cv, (330, 709), text="English",
                 fontsize=17, family=FONT_FAMILY_BOLD)
    button = maliang.Button(cv, (50, 700), size=(100, 40), command=lambda: changeWindow(mainPage), fontsize=16,
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

    maliang.CheckBox(cv, (50, 600), command=agreeLicense,
                     default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(
        cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(
        cv, (170, 705), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    changeLanguage('cn')

    root.mainloop()


def aboutPage():
    cv = createPage()

    maliang.IconButton(
        cv,
        position=(50, 50),
        size=(50, 50),
        command=lambda: changeWindow(settingsPage),
        image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1))
    )

    maliang.Text(cv, (110, 50), text=translate("settings"),
                 family=FONT_FAMILY_LIGHT, fontsize=15)
    maliang.Text(cv, (110, 70), text=translate("about"),
                 family=FONT_FAMILY_BOLD, fontsize=26)

    # 居中放置logo
    logo_size = 120
    icon_x = 250 - (logo_size // 2)
    icon_y = 150

    maliang.IconButton(
        cv,
        position=(icon_x, icon_y),
        size=(logo_size, logo_size),
        image=ImageTk.PhotoImage(getImage('icon_logo').resize((logo_size, logo_size), 1)),
        command=lambda: openGithub('the-OmegaLabs/ArkLauncher')
    )

    # 调整文本位置以匹配图片
    maliang.Text(
        cv,
        (250, 300),
        text="Artistic Network",
        family=FONT_FAMILY_LIGHT,
        fontsize=20,
        anchor='center'
    )

    maliang.Text(
        cv,
        (250, 340),
        text="ArkLauncher",
        family=FONT_FAMILY_BOLD,
        fontsize=36,
        anchor='center'
    )

    # 修改版本格式为 "Developing Version 25w33a"
    maliang.Text(
        cv,
        (250, 380),
        text=f"Version {_VERSION}{_SUBVERSION}",
        family=FONT_FAMILY,
        fontsize=15,
        anchor='center'
    )

    # 添加版权文本
    maliang.Text(
        cv,
        (250, 420),
        text=translate("open_source_notice"),
        family=FONT_FAMILY,
        fontsize=12,
        anchor='center'
    )

    maliang.Text(
        cv,
        (250, 440),
        text="©2025 Artistic Network™",
        family=FONT_FAMILY,
        fontsize=12,
        anchor='center'
    )

    # 贡献者部分标题
    maliang.Text(
        cv,
        (250, 480),
        text=translate("contributors"),
        family=FONT_FAMILY_BOLD,
        fontsize=26,
        anchor='center'
    )

    # 贡献者信息
    contributors = [
        {
            'name': 'Stevesuk0',
            'contribution': translate('leaddev'),
            'github': 'Stevesuk0'
        },
        {
            'name': 'bzym2',
            'contribution': translate('deve'),
            'github': 'bzym2'
        },
        {
            'name': 'HRGC-Sonrai',
            'contribution': translate('ud+dev'),
            'github': 'HRGC-Sonrai'
        }
    ]

    # 增加间距以容纳名称和贡献
    avatar_size = 50
    avatar_spacing = 120  # 增加间距以容纳文本
    total_width = (len(contributors) - 1) * avatar_spacing + avatar_size

    start_x = 250 - (total_width // 2)
    avatar_y = 520

    for i, contributor in enumerate(contributors):
        x_pos = start_x + (i * avatar_spacing)
        x_center = x_pos + (avatar_size // 2)

        # 头像
        if contributor['github'] in images['contributors']:
            maliang.IconButton(
                cv,
                position=(x_pos, avatar_y),
                size=(avatar_size, avatar_size),
                command=lambda c=contributor['github']: openGithub(c),
                image=ImageTk.PhotoImage(
                    getImage(contributor['github'], category='contributors').resize((47, 47), 1))
            )

        # 名称
        maliang.Text(
            cv,
            (x_center, avatar_y + avatar_size + 15),
            text=contributor['name'],
            family=FONT_FAMILY_BOLD,
            fontsize=14,
            anchor='center'
        )

        # 贡献
        maliang.Text(
            cv,
            (x_center, avatar_y + avatar_size + 35),
            text=contributor['contribution'],
            family=FONT_FAMILY_LIGHT,
            fontsize=12,
            anchor='center'
        )

    root.mainloop()


def mainPage():
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

    backgroundImage = getImage('ChiesaBianca', 'background')

    background = maliang.Image(cv, position=(0, 0), size=(
        WIDTH, HEIGHT), image=ImageTk.PhotoImage(backgroundImage))

    upHEIGHT            = 65
    topImage            = maliang.Image(cv, position=(0, 0), image=ImageTk.PhotoImage(makeImageBlur(backgroundImage.crop((0, 0, WIDTH, upHEIGHT)), radius=10)))
    topMask             = maliang.Image(cv, position=(0, 0), image=ImageTk.PhotoImage(makeImageMask(size=(WIDTH, upHEIGHT))))
    topIconMask         = maliang.Image(topMask, position=(0, 0),image=ImageTk.PhotoImage(makeImageMask(size=(upHEIGHT, upHEIGHT), color=(0, 0, 0, 16))))
    topSearchMask       = maliang.Image(topMask, position=(upHEIGHT, 0), image=ImageTk.PhotoImage(makeImageMask(size=(int(WIDTH - (upHEIGHT * 3)), upHEIGHT), color=(0, 0, 0, 50))))
    topMinimizeMask     = maliang.Image(topMask, position=(int(WIDTH - (upHEIGHT * 2)), 0), image=ImageTk.PhotoImage(makeImageMask((upHEIGHT, upHEIGHT), color=(0, 0, 0, 80))))
    topExitMask         = maliang.Image(topMask, position=(int(WIDTH - (upHEIGHT * 1)), 0), image=ImageTk.PhotoImage(makeImageMask((upHEIGHT, upHEIGHT), color=(120, 0, 0, 128))))

    bottomHEIGHT        = 200
    bottomMaskHEIGHT    = 70
    bottomLMaskHEIGHT   = 130
    bottomImage         = maliang.Image(cv, position=(0, 600), image=ImageTk.PhotoImage(makeImageBlur(backgroundImage.crop((0, HEIGHT - bottomHEIGHT, WIDTH, HEIGHT)), radius=10)))
    bottomMask          = maliang.Image(cv, position=(0, 600), image=ImageTk.PhotoImage(makeImageMask(size=(HEIGHT, bottomHEIGHT))))
    bottomSettingsMask  = maliang.Image(bottomMask, position=(bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=ImageTk.PhotoImage(makeImageRadius(makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
    bottomAccountMask   = maliang.Image(bottomMask, position=(500 - bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=ImageTk.PhotoImage(makeImageRadius(makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
    bottomSubMask       = maliang.Image(bottomMask, position=(0, bottomMaskHEIGHT), image=ImageTk.PhotoImage(makeImageMask((WIDTH, bottomLMaskHEIGHT), color=(0, 0, 0, 64))))
    bottomLaunchMask    = maliang.Image(bottomSubMask, position=(10, 7), image=ImageTk.PhotoImage(makeImageMask((480, 116), color=(0, 0, 0, 64))))

    logo                = maliang.IconButton(topIconMask, size=(upHEIGHT, upHEIGHT), position=(upHEIGHT // 2, upHEIGHT // 2 + 2), image=ImageTk.PhotoImage(getImage('icon_logo').resize((40, 40), 1)), anchor='center')
    searchBox           = maliang.InputBox(topSearchMask, position=(0, 2), size=(int(WIDTH - (upHEIGHT * 3)), upHEIGHT - 4), placeholder=translate('search'), family=FONT_FAMILY_BOLD, fontsize=18)
    minimize            = maliang.IconButton(topMinimizeMask, (2, 2), (upHEIGHT - 4, upHEIGHT - 4), image=ImageTk.PhotoImage(getImage('icon_minimize').resize((40, 40), 1)), command=minimizeWindow)
    exit                = maliang.IconButton(topExitMask, (2, 2), (upHEIGHT - 4, upHEIGHT - 4), image=ImageTk.PhotoImage(getImage('icon_exit').resize((40, 40), 1)), command=minimizeAndExit)
 
    settings            = maliang.IconButton(bottomSettingsMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=ImageTk.PhotoImage(getImage('icon_settings').resize((40, 40), 1)), command=lambda: changeWindow(settingsPage), anchor='center')
    account             = maliang.IconButton(bottomAccountMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=ImageTk.PhotoImage(getImage('icon_account').resize((40, 40), 1)), command=lambda: changeWindow(settingsAccountPage), anchor='center')

    launch              = maliang.Button(bottomLaunchMask, (0, 0), size=(480, 116))
    launchIcon          = maliang.Image(launch, (bottomLMaskHEIGHT // 2 - 5, bottomLMaskHEIGHT // 2 - 7),image=ImageTk.PhotoImage(getImage('icon_launch').resize((80, 80), 1)), anchor='center')
    launchDesc          = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 35), text='启动游戏', family=FONT_FAMILY,fontsize=17)
    launchTitle         = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 10), text='Meira Client', family=FONT_FAMILY_BOLD, fontsize=25)

    launch.style.set(fg=('', '', ''), bg=('', '', ''), ol=('#4C4849', '#BBBBBB'))
    account.style.set(bg=_EMPTY, ol=_EMPTY)
    settings.style.set(bg=_EMPTY, ol=_EMPTY)
    logo.style.set(bg=_EMPTY, ol=_EMPTY)
    exit.style.set(bg=('', '#990000', ''), ol=('', '#EEEEEE'))
    minimize.style.set(bg=('', '#024477', ''), ol=('', '#EEEEEE'))
    searchBox.style.set(bg=_EMPTY, ol=_EMPTY)

    root.bind("<ButtonPress-1>", focusWindow)
    # logo.bind("<B1-Motion>", on_drag_motion)

    root.mainloop()


def settingsPage():
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(mainPage))

    backgroundImage = mergeImage(makeImageBlur(getImage('ChiesaBianca', 'background'), radius=25),
                                 makeImageMask((500, 800), (0, 0, 0, 96)))

    background = maliang.Image(cv, position=(0, 0), size=(500, 800), image=ImageTk.PhotoImage(backgroundImage))

    root.mainloop()


def settingsAccountPage():
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(settingsPage))

    text_logo1 = maliang.Text(
        cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(
        cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('account'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage),
                       image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1)))

    needLogin_text1 = maliang.Text(cv, position=(
        250, 345), anchor='center', family=FONT_FAMILY, fontsize=26)
    needLogin_text2 = maliang.Text(cv, position=(
        250, 390), anchor='center', family=FONT_FAMILY_BOLD, fontsize=30)
    needLogin_text3 = maliang.Text(cv, position=(
        250, 423), anchor='center', family=FONT_FAMILY, fontsize=12)

    loginButton = maliang.Button(cv, position=(250, 460), size=(
        80, 40), anchor='center', family=FONT_FAMILY, fontsize=17)

    needLogin_text1.set(translate('needLogin1'))
    needLogin_text2.set(translate('needLogin2'))
    needLogin_text3.set(translate('needLogin3'))
    loginButton.set(translate('login'))

    root.mainloop()


def settingsNetworkPage():
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(settingsPage))

    text_logo1 = maliang.Text(
        cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(
        cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('network'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage),
                       image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1)))

    # noticeLabel = maliang.Label(cv, position=(50, 165), size=(400, 80), family=FONT_FAMILY, fontsize=15)
    # noticeLabel.set('When you launch your Minecraft instance using ArkLa\nuncher, We will automatically take over Minecraft\'s ne\ntwork and attempt to accelerate it.')

    # label = maliang.Label(cv, position=(50, 500), size=(400, 100))

    root.mainloop()


def settingsCustomizePage():
    global _THEME
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(settingsPage))

    text_logo1 = maliang.Text(
        cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(
        cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('customize'))

    first = False

    colorLabel = maliang.Button(cv, position=(50, 150), size=(
        400, 177), family=FONT_FAMILY, fontsize=15)

    def updateWidget(*_):
        nonlocal colorLabel

        colorLabelText = maliang.Text(colorLabel, position=(
            5, -30), family=FONT_FAMILY, fontsize=15)

        HEIGHT = 5
        buttonDark = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55),
                                        command=lambda: changeTheme('dark'),
                                        family=FONT_FAMILY_BOLD,
                                        image=ImageTk.PhotoImage(getImage('icon_dark').resize((40, 40), 1)),
                                        fontsize=18)
        HEIGHT += 56
        buttonLight = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55),
                                         command=lambda: changeTheme('light'), family=FONT_FAMILY_BOLD,
                                         image=ImageTk.PhotoImage(
                                             getImage('icon_light').resize((40, 40), 1)),
                                         fontsize=18)
        HEIGHT += 56
        buttonSystem = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55),
                                          command=lambda: changeTheme('system'), family=FONT_FAMILY_BOLD,
                                          image=ImageTk.PhotoImage(
                                              getImage('icon_auto').resize((40, 40), 1)),
                                          fontsize=18)

        maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage),
                           image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1)))

        colorLabelText.set(translate('color'))

        buttonDark.set(translate('dark'))
        buttonLight.set(translate('light'))
        buttonSystem.set(translate('auto'))

    def changeTheme(theme, style):
        global _THEME, root
        nonlocal first, colorLabel

        if first:
            colorLabel.destroy()
            colorLabel = maliang.Button(cv, position=(50, 150), size=(
                400, 177), family=FONT_FAMILY, fontsize=15)

        _THEME = theme

        maliang.theme.manager.set_color_mode(_THEME)

        configLib.setConfig('theme', _THEME)
        configLib.sync()

        refreshImage(threaded=True)
        maliang.IconButton(cv, position=(50, 50), size=(50, 40), command=lambda: changeWindow(settingsPage),
                           image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1)))

        updateWidget()

        log(f"Instant change widget to {_THEME} style.", type=olog.Type.DEBUG)

        first = True

    maliang.theme.manager.register_event(updateWidget)
    # maliang.theme.manager.register_event(changeTheme, (darkdetect.theme(), _STYLE))

    updateWidget(_THEME)

    root.mainloop()


def settingsLanguagePage():
    global locale, FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT
    cv = createPage()
    cv.bind("<Escape>", lambda event: changeWindow(settingsPage))

    text_logo1 = maliang.Text(
        cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(
        cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('locale'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage),
                       image=ImageTk.PhotoImage(getImage('icon_return').resize((55, 55), 1)))

    HEIGHT = 5
    lang_changebutton = []

    Label = maliang.Button(cv, position=(50, 165), size=(
        400, 10 + len(getImage('country')) * 56), family=FONT_FAMILY, fontsize=15)

    def setLanguage(lang):
        global locale

        locale = lang

        log(f'Change language to \"{locale}\".')

        updateFont()
        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))

    for i in lang_dict:
        lang_changebutton.append(
            maliang.IconButton(
                Label,
                position=(5, HEIGHT),
                size=(390, 55),
                command=lambda lang=i: setLanguage(lang),
                image=ImageTk.PhotoImage(
                    getImage(i, category='country').resize((40, 40), 1)),
                family=FONT_FAMILY_BOLD,
                fontsize=18,
                text=lang_dict[i]['self'],
            )
        )
        HEIGHT += 56

    root.mainloop()


def tracebackWindow(exception: Exception):
    log('Starting Traceback window because a exception detected.', type=olog.Type.WARN)

    tracelist = ''.join(traceback.format_exception(exception)).split('\n')

    for i in tracelist[:-1]:
        log(i, type=olog.Type.ERROR)

    width = 1000
    height = len(tracelist[:-1]) * 20 + 200
    root = maliang.Tk(size=(width, height),
                      title=f'ArkLauncher traceback window | {_VERSION}')
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
    root.center()
    root.mainloop()


try:
    refreshImage(threaded=False)

    hidden_menu = (
        LightTray.MenuItem('Focus', focusWindow, default=True),
        LightTray.Menu.SEPARATOR,
        LightTray.MenuItem('Exit', minimizeAndExit)
    )

    icon = LightTray.Icon("name", getImage('icon_logo'),
                        "ArkLauncher Tray", menu=hidden_menu)

    threading.Thread(target=icon.run, daemon=True).start()

    loadLocale()
    updateFont()  # auto select font

    endLoadTime = time.time() - startLoadTime

    createRoot()

    focusWindow()

    log(f'Loaded ArkLauncher in {int(endLoadTime * 1000)}ms.')

    if configLib.first:
        welcomePage()
    else:
        mainPage()

except Exception as f:
    tracebackWindow(f)
