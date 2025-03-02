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


_VERSION = 'dev'
_SUBVERSION = '25w10a'

import time
startLoadTime = time.time()

# base
from io import BytesIO
from datetime import datetime
from PIL import Image
import json
import os
import platform
import threading
import traceback
import colorama
import darkdetect
import maliang
import maliang.animation
import maliang.core
import maliang.color
import maliang.standard
import maliang.theme
import maliang.toolbox
import ctypes
import socket
import requests
import gc

# customed
import libs.config as configLib
from libs import olog as olog
from libs.olog import output as log

hwnd = ctypes.windll.user32.GetForegroundWindow()   
user32 = ctypes.windll.user32
user32.SetWindowTextW(hwnd, f'ArkLauncher Console Interface - {_VERSION}, {_SUBVERSION}.')

# config
WIDTH = 500
HEIGHT = 800

configLib.loadConfig()
config = configLib.config
locale = config['language']

images = {}
_FONTS = []
_THEME = config['theme']
_BORDER = config['border']
_SYSTEM = platform.system()
#_STYLE = maliang.configs.Env.get_default_system()
_STYLE = config['style']
maliang.configs.Env.system = _STYLE
maliang.theme.manager.set_color_mode(_THEME)


if _SYSTEM == 'Windows':
    import libs.avatar.Windows as avatar
elif _SYSTEM == 'Linux':
    import libs.avatar.Linux as avatar

olog.logLevel = 5

log(f'Starting ArkLauncher GUI, version {_VERSION}-{_SUBVERSION}.')

colorama.init()

def testDragAndDrop(*args):
    log(f'dnd: {args}')


def loadFont(fontPath):
    global _FONTS
    if not fontPath in _FONTS:
        _FONTS.append(fontPath)
        maliang.toolbox.load_font(fontPath, private=True) # must be private.
        log(f'Loaded font \"{fontPath}\".')

def testConnection():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except Exception as e:
        return False    

def getSourceContent(url):
    olog.output(f'Sending requests to {url}/metadata.json...')
    response = requests.get(f'{url}/metadata.json')
    metadata = response.json()
    log(f'Response from remote: {metadata}', type=olog.Type.DEBUG)
    
    log(f'Sending requests to: {url}/{metadata['icon']}', type=olog.Type.DEBUG)
    image = requests.get(f'{url}{metadata['icon']}')
    metadata['icon'] = Image.open(BytesIO(image.content))
    return (True, metadata)

def updateFont():
    global FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT
    
    
    for i in os.listdir('src/font'):
        loadFont(f'src/font/{i}')
        
    log(f'Loaded {len(os.listdir('src/font'))} fonts.')

    if locale == 'en':
        FONT_FAMILY = 'Segoe UI'
        FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
        FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
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
    

def refreshImage(*args):
    global images

    del images
    gc.collect()

    def loadImage(path):
        try:
            img = Image.open(path)
            return img
        except Exception as e:
            print(f"Error loading image {path}: {e}")
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
            log(f"Loaded image: {path}")

    theme = darkdetect.theme().lower() if _THEME == 'system' else _THEME

    # Initialize images dictionary with categories
    images = {
        'contributors': {},
        'country': {}
    }

    # Define image paths with categories
    image_paths = {
        'contributors': {
            'maliang':        f'src/icon/contributors/maliang.png',
            'Stevesuk0':      f'src/icon/contributors/Stevesuk0.png',
            'bzym2':          f'src/icon/contributors/bzym2.png',
            'HRGC-Sonrai':    f'src/icon/contributors/HRGC-Sonrai.png',
            'the-OmegaLabs':  f'src/icon/contributors/the-OmegaLabs.png',
        },
        'country': {
            'cn':             f'src/icon/both/country_cn.png',
            'jp':             f'src/icon/both/country_jp.png',
            'ko':             f'src/icon/both/country_ko.png',
            'en':             f'src/icon/both/country_us.png',
            'sb':             f'src/icon/both/transgender.png',
            'ug':             f'src/icon/both/country_cn.png'
        },
        None: {  # Regular images without category
            'icon_quick':     f'src/icon/both/quick.png',
            'icon_logo':      f'src/icon/main.png',
            'icon_return':    f'src/icon/{theme}/return.png',
            'icon_settings':  f'src/icon/{theme}/settings.png',
            'icon_about':     f'src/icon/{theme}/about.png',
            'icon_language':  f'src/icon/{theme}/language.png',
            'icon_network':   f'src/icon/{theme}/network.png',
            'icon_account':   f'src/icon/{theme}/account.png',
            'icon_customize': f'src/icon/{theme}/customize.png',
            'icon_dark':      f'src/icon/{theme}/dark.png',
            'icon_light':     f'src/icon/{theme}/light.png',
            'icon_auto':      f'src/icon/{theme}/auto.png',
            'icon_info':      f'src/icon/{theme}/info.png',
            'icon_round':     f'src/icon/{theme}/round.png',
            'icon_square':    f'src/icon/{theme}/square.png',
        }
    }

    # Load all images with their respective categories
    for category, items in image_paths.items():
        for key, path in items.items():
            threading.Thread(
                target=threadedImageOpen,
                args=(path, key, category)
            ).start()
    
    log(f'Loaded {len(image_paths['contributors']) + len(image_paths["country"]) + len(image_paths[None])} images.')


def openGithub(name):
    os.system(f'start https://github.com/{name}')


def createWindow(x=None, y=None):
    log(f'Creating new page at ({x}, {y}).', type=olog.Type.DEBUG)
    if x and y:
        root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y),
                            title=f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')
    else:
        root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')

    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.minsize(WIDTH, HEIGHT)
    root.maxsize(WIDTH, HEIGHT)
    maliang.theme.manager.customize_window(root, disable_maximize_button=True, border_type=_BORDER)

    maliang.theme.manager.apply_file_dnd(window=root, command=testDragAndDrop)
    root.icon(maliang.PhotoImage(images['icon_logo'].resize((32, 32), 1)))
    return root, cv


def changeWindow(window, root: maliang.Tk):
    log(f'Perform change window to "{window.__name__}"...', type=olog.Type.INFO)
    x, y = root.winfo_x(), root.winfo_y()
    if platform.system() == 'Linux':
        x -= 5
        y -= 31
    root.__exit__()
    del root
    gc.collect()
    window(x, y)


def welcomePage():
    global locale
    root, cv = createWindow()

    FONT_FAMILY_BOLD = 'Microsoft YaHei UI Bold'

    maliang.Image(cv, (50, 75), image=maliang.PhotoImage(images['icon_logo'].resize((150, 150), 1)))
    text_welcome = maliang.Text(cv, (50, 250), family=FONT_FAMILY_BOLD, fontsize=30)
    text_desc = maliang.Text(cv, (50, 300), family=FONT_FAMILY_BOLD, fontsize=17)
    text_license = maliang.Text(cv, (85, 605), family=FONT_FAMILY_BOLD, fontsize=15)
    text_collect = maliang.Text(cv, (85, 643), family=FONT_FAMILY_BOLD, fontsize=15)
    text_button_chinese = maliang.Text(cv, (210, 709), text="中文", fontsize=17, family=FONT_FAMILY_BOLD)
    maliang.Text(cv, (330, 709), text="English", fontsize=17, family=FONT_FAMILY_BOLD)
    button = maliang.Button(cv, (50, 700), size=(100, 40), command=lambda: changeWindow(mainPage, root), fontsize=16,
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

    maliang.CheckBox(cv, (50, 600), command=agreeLicense, default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    changeLanguage('cn')

    root.mainloop()

def aboutPage(x, y):
    root, cv = createWindow(x, y)

    maliang.IconButton(
        cv,
        position=(50, 50),
        size=(50, 50),
        command=lambda: changeWindow(settingsPage, root),
        image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1))
    )

    maliang.Text(cv, (110, 50), text=translate("settings"), family=FONT_FAMILY_LIGHT, fontsize=15)
    maliang.Text(cv, (110, 70), text=translate("about"), family=FONT_FAMILY_BOLD, fontsize=26)

    icon_x = 250 - (120 // 2)

    maliang.IconButton(
        cv,
        position=(icon_x, 120),
        size=(120, 120),
        image=maliang.PhotoImage(images['icon_logo'].resize((120, 120), 1)),
        command=lambda: openGithub('the-OmegaLabs/ArkLauncher')
    )

    maliang.Text(
        cv,
        (250, 270),
        text="Artistic Network",
        family=FONT_FAMILY_LIGHT,
        fontsize=20,
        anchor='center'
    )
    maliang.Text(
        cv,
        (250, 300),
        text="ArkLauncher",
        family=FONT_FAMILY_BOLD,
        fontsize=32,
        anchor='center'
    )
    maliang.Text(
        cv,
        (250, 330),
        text=f"Version: {translate(_VERSION)}-{_SUBVERSION}",
        family=FONT_FAMILY,
        fontsize=15,
        anchor='center'
    )

    maliang.Text(
        cv,
        (250, 400),
        text=translate("contributors"),
        family=FONT_FAMILY_BOLD,
        fontsize=26,
        anchor='center'
    )

    avatar_size = 50
    avatar_spacing = 60
    contributors = ['Stevesuk0', 'bzym2', 'HRGC-Sonrai']
    total_width = (len(contributors) - 1) * avatar_spacing + avatar_size

    start_x = 250 - (total_width // 2)

    for i, contributor in enumerate(contributors):
        x_pos = start_x + (i * avatar_spacing)
        if contributor in images['contributors']:
            maliang.IconButton(
                cv,
                position=(x_pos, 430),
                size=(avatar_size, avatar_size),
                command=lambda c=contributor: openGithub(c),
                image=maliang.PhotoImage(images['contributors'][contributor].resize((47, 47), 1))
                )

    root.mainloop()


def mainPage(x, y):
    root, cv = createWindow(x, y)

    def getTimeBasedGreeting():
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            return translate('good_morning')
        elif 12 <= current_hour < 18:
            return translate('good_afternoon')
        elif 18 <= current_hour < 22:
            return translate('good_evening')
        else:
            return translate('good_night')

    def createNotice(str, sub, cv, spin):
        noticeBar = maliang.Label(master=cv, size=(320, 70), position=(90, 800))
        noticeText = maliang.Text(noticeBar, (65, 15), text=str, family=FONT_FAMILY_BOLD, fontsize=14)
        maliang.Text(noticeBar, (65, 36), text=sub, family=FONT_FAMILY, fontsize=14)

        if spin == True:
            noticeSpinner = maliang.Spinner(noticeBar, (35, 35), mode="indeterminate", anchor='center')
            return [noticeBar, noticeText, noticeSpinner]
        else:
            return [noticeBar, noticeText]

    def playToastAnimation():
        nonlocal animation
        animation.start(delay=150)

    def stopAniAndChangeWindow(window: object, root: maliang.Tk):
        nonlocal animation
        animation.stop()
        animation = maliang.animation.MoveWidget(noticeBar, offset=(0, 100), duration=200,
                                            controller=maliang.animation.ease_in, fps=1000,
                                            end=lambda: (animation.stop(), changeWindow(window, root)))
        animation.start()

        #changeWindow(window, root)
        

    icon_x = 50
    icon_y = 50
    icon_size = 50
    logo = maliang.Image(cv, (icon_x, icon_y),
                              image=maliang.PhotoImage(images['icon_logo'].resize((icon_size, icon_size), 1)))

    greeting_text = maliang.Text(cv, (58, 115),
                                 family=FONT_FAMILY_BOLD,
                                 fontsize=24)
    
    greeting_text.set(getTimeBasedGreeting())

    content_start_y = 165

    button_new = maliang.Button(cv, position=(50, content_start_y), size=(400, 100))
    maliang.Text(button_new, (200, 50), text='+', family=FONT_FAMILY_BOLD, fontsize=50, anchor='center')

    maliang.Tooltip(
        maliang.IconButton(cv, position=(400, 50), size=(50, 50),
                           command=lambda: stopAniAndChangeWindow(settingsPage, root),
                           image=maliang.PhotoImage(images['icon_settings'].resize((55, 55), 1))),
        text=translate('settings'), 
        family=FONT_FAMILY, 
        fontsize=13)

    maliang.Tooltip(
        maliang.IconButton(cv, position=(340, 50), size=(50, 50),
                           command=lambda: stopAniAndChangeWindow(mainPage, root),
                           image=maliang.PhotoImage(images['icon_quick'].resize((40, 40), 1))),
        text=translate('quick'),
        family=FONT_FAMILY,
        fontsize=13)

    noticeBar, _, _ = createNotice(f"{translate('logging_in')} {translate('parent')}...",
                                   translate('wait'), cv, 1)
        
    animation = maliang.animation.MoveWidget(noticeBar, offset=(0, -100), duration=500,
                                            controller=maliang.animation.ease_out, fps=1000)

    playToastAnimation()
    root.mainloop()


def settingsPage(x, y):
    root, cv = createWindow(x, y)
    
    
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['icon_account'].resize((45, 45), 1)))

    Label = maliang.Button(cv, position=(50, 165), size=(400, 290), family=FONT_FAMILY, fontsize=15)
    HEIGHT = 5
    button_account = maliang.IconButton(Label, position=(5, HEIGHT), size=(390, 55),
                                        command=lambda: changeWindow(settingsAccountPage, root),
                                        image=maliang.PhotoImage(images['icon_account'].resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 56
    button_language = maliang.IconButton(Label, position=(5, HEIGHT), size=(390, 55),
                                         command=lambda: changeWindow(settingsLanguagePage, root),
                                         image=maliang.PhotoImage(images['icon_language'].resize((40, 40), 1)),
                                         family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 56
    button_network = maliang.IconButton(Label, position=(5, HEIGHT), size=(390, 55),
                                        command=lambda: changeWindow(settingsNetworkPage, root),
                                        image=maliang.PhotoImage(images['icon_network'].resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 56
    button_customize = maliang.IconButton(Label, position=(5, HEIGHT), size=(390, 55),
                                          command=lambda: changeWindow(settingsCustomizePage, root),
                                          image=maliang.PhotoImage(images['icon_customize'].resize((40, 40), 1)),
                                          family=FONT_FAMILY_BOLD,
                                          fontsize=18)
    HEIGHT += 56
    button_about = maliang.IconButton(Label, position=(5, HEIGHT), size=(390, 55),
                                      command=lambda: changeWindow(aboutPage, root),
                                      image=maliang.PhotoImage(images['icon_about'].resize((40, 40), 1)),
                                      family=FONT_FAMILY_BOLD,
                                      fontsize=18)

    text_logo1.set(translate('homepage'))
    text_logo2.set(translate('settings'))
    button_account.set(f" {translate('account')}")
    button_language.set(f" {translate('locale')}")
    button_network.set(f" {translate('network')}")
    button_about.set(f" {translate('about')}")
    button_customize.set(f" {translate('customize')}")

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root),
                       image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

    root.mainloop()


def settingsAccountPage(x, y):
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('account'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

    root.mainloop()


def settingsNetworkPage(x, y):
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('network'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))
    

    #noticeLabel = maliang.Label(cv, position=(50, 165), size=(400, 80), family=FONT_FAMILY, fontsize=15)
    #noticeLabel.set('When you launch your Minecraft instance using ArkLa\nuncher, We will automatically take over Minecraft\'s ne\ntwork and attempt to accelerate it.')


    #label = maliang.Label(cv, position=(50, 500), size=(400, 100))

    root.mainloop()



def settingsCustomizePage(x, y):
    global _THEME
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('customize'))

    first = False
    
    colorLabel = maliang.Button(cv, position=(50, 150), size=(400, 177), family=FONT_FAMILY, fontsize=15)
    styleLabel = maliang.Button(cv, position=(50, 392), size=(400, 177), family=FONT_FAMILY, fontsize=15)

    def updateWidget(*_):
        nonlocal colorLabel, styleLabel
        
        colorLabelText = maliang.Text(colorLabel, position=(5, -30), family=FONT_FAMILY, fontsize=15)

        HEIGHT = 5
        buttonDark = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55), command=lambda: changeTheme('dark', _STYLE),
                                        family=FONT_FAMILY_BOLD,
                                        image=maliang.PhotoImage(images['icon_dark'].resize((40, 40), 1)), fontsize=18)
        HEIGHT += 56
        buttonLight = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55),
                                        command=lambda: changeTheme('light', _STYLE), family=FONT_FAMILY_BOLD,
                                        image=maliang.PhotoImage(images['icon_light'].resize((40, 40), 1)),
                                        fontsize=18)
        HEIGHT += 56
        buttonSystem = maliang.IconButton(colorLabel, position=(5, HEIGHT), size=(390, 55),
                                        command=lambda: changeTheme('system', _STYLE), family=FONT_FAMILY_BOLD,
                                        image=maliang.PhotoImage(images['icon_auto'].resize((40, 40), 1)),
                                        fontsize=18)

        maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                        image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

        styleLabelText = maliang.Text(styleLabel, position=(5, -30), family=FONT_FAMILY, fontsize=15)

        HEIGHT = 5
        maliang.Env.system = 'Windows10'
        button10 = maliang.IconButton(styleLabel, position=(5, HEIGHT), size=(390, 55), command=lambda: changeTheme(theme=_THEME, style='Windows10'),
                                        family=FONT_FAMILY_BOLD,
                                        image=maliang.PhotoImage(images['icon_square'].resize((40, 40), 1)), fontsize=18)
        HEIGHT += 56
        maliang.Env.system = 'Windows11'
        button11 = maliang.IconButton(styleLabel, position=(5, HEIGHT), size=(390, 55),
                                         command=lambda: changeTheme(theme=_THEME, style='Windows11'), family=FONT_FAMILY_BOLD,
                                         image=maliang.PhotoImage(images['icon_round'].resize((40, 40), 1)),
                                         fontsize=18)
        HEIGHT += 56
        maliang.Env.system = _STYLE
        buttonSystem2 = maliang.IconButton(styleLabel, position=(5, HEIGHT), size=(390, 55),
                                          command=lambda: changeTheme(theme=_THEME, style=maliang.configs.Env.get_default_system()), family=FONT_FAMILY_BOLD,
                                          image=maliang.PhotoImage(images['icon_auto'].resize((40, 40), 1)),
                                          fontsize=18)
        
        colorLabelText.set(translate('color'))
        styleLabelText.set(translate('style'))

        buttonDark.set(translate('dark'))
        buttonLight.set(translate('light'))
        buttonSystem.set(translate('auto'))

        button10.set(translate('square'))
        button11.set(translate('round'))
        buttonSystem2.set(translate('auto'))

    def changeTheme(theme, style):
        global _THEME, _STYLE
        nonlocal first, root, colorLabel, styleLabel
        
        if first:
            colorLabel.destroy()
            styleLabel.destroy()
            colorLabel = maliang.Button(cv, position=(50, 150), size=(400, 177), family=FONT_FAMILY, fontsize=15)
            styleLabel = maliang.Button(cv, position=(50, 392), size=(400, 177), family=FONT_FAMILY, fontsize=15)

        _THEME = theme
        _STYLE = style
        
        maliang.theme.manager.set_color_mode(_THEME)
        maliang.Env.system = style

        configLib.setConfig('theme', _THEME)
        configLib.setConfig('style', _STYLE)
        configLib.sync()

        log(f"Changing window to {_THEME} style.", type=olog.Type.INFO)
        refreshImage()
        maliang.IconButton(cv, position=(50, 50), size=(50, 40), command=lambda: changeWindow(settingsPage, root),
                        image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

        updateWidget()

        log(f"Instant change widget to {_THEME} style.", type=olog.Type.DEBUG)
        
        first = True
    
    maliang.theme.manager.register_event(refreshImage)
    maliang.theme.manager.register_event(updateWidget)
    #maliang.theme.manager.register_event(changeTheme, (darkdetect.theme(), _STYLE))

    changeTheme(_THEME, _STYLE)


    root.mainloop()


def loadLocale():
    global lang_dict

    lang_dict = {}

    for i in os.listdir('./src/lang'):
        if i.endswith('.json'):
            with open(f'./src/lang/{i}', encoding='utf-8') as f:
                lang_dict[i[:-5]] = json.loads(f.read())
                
            log(f'Loaded locale file "{i}"...')


def translate(target):
    return lang_dict.get(locale, {}).get(target, lang_dict['en'].get(target, target))


def settingsLanguagePage(x, y):
    global locale, FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('locale'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

    HEIGHT = 5
    lang_changebutton = []

    Label = maliang.Button(cv, position=(50, 165), size=(400, 10 + len(images['country']) * 56), family=FONT_FAMILY, fontsize=15)

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
                image=maliang.PhotoImage(images['country'][i].resize((40, 40), 1)),
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
    root = maliang.Tk(size=(width, height), title=f'ArkLauncher {_VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=width, height=height)

    text_title = maliang.Text(cv, (50, 50), fontsize=23)
    text_title.set('An error detected.')

    text_title = maliang.Text(cv, (50, 80), fontsize=17)
    text_title.set('You can take an screenshot in this window, and send it to the author.')

    text_trace = maliang.Text(cv, (50, 130), fontsize=14)
    text_trace.set(str(''.join(traceback.format_exception(exception))))

    root.at_exit(exit)
    root.center()
    root.mainloop()


try:
    refreshImage()
    loadLocale()
    updateFont() # auto select font

    endLoadTime = time.time() - startLoadTime

    log(f'Loaded ArkLauncher in {int(endLoadTime * 1000)}ms.')
    if configLib.first:
        welcomePage()
    else:
        mainPage(710, 200)

except Exception as f:
    tracebackWindow(f)
