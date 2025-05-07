# Copyright 2025 Omega Labs, ArkLauncher Contributors.
# Report bugs and issues to https://github.com/the-OmegaLabs/ArkLauncher/issues
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
3
# The Dash Imaging Library (fork from PIL).
#
# License:
# This project is licensed under multiple licenses:
#
# Apache License 2.0: The new modifications and additions made by Omega Labs and ArkLauncher Contributors.
#
# Copyright (c) 2025 Omega Labs, ArkLauncher Contributors.
#
# Partial icensed under the Apache License, Version 2.0 (the "License");
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
#
# MIT License: Portions of the code derived from the original PIL (Python Imaging Library), created by Secret Labs AB and Fredrik Lundh.
#
# Copyright (c) 1997-2009 by Secret Labs AB.  All rights reserved.
# Copyright (c) 1995-2009 by Fredrik Lundh.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Some of the sound effects used in this project are sourced from Apple’s macOS system.
# All copyrights and trademarks remain the property of Apple Inc. These assets are used solely 
# for educational, research, or non-commercial demonstration purposes. 
# No commercial use or distribution is intended.
#
# If Apple Inc. or any rights holder believes that the use of these assets is inappropriate, 
# please contact our team, and I will promptly remove or replace the material as requested.

__version__ = 'dev'
__subversion__ = '25w19b'
__author__ = [ # Sorted by contributions 
    "Stevesuk0 (stevesukawa@outlook.com)",
    "bzym2 (mantouk@qq.com)",
    "HRGC-Sonrai",
    "PPicku"
]

def tracebackWindow(exception: Exception):
    os.makedirs('dumps', exist_ok=True)

    def isSerializable(obj) -> bool:
        try:
            json.dumps(obj)
            return True
        except TypeError:
            return False
        
    tracelist = ''.join(traceback.format_exception(exception)).split('\n')

    width = max(len(item) for item in tracelist) * 8 + 150
    height = len(tracelist[:-1]) * 20 + 150
    
    try:
        Utils.play('error')
    except:
        pass

    nowTime = time.time()
    globalsFiltered = {
        key: value for key, value in globals().items() if isSerializable(value)
    }
    globalsFiltered.update({
        'systemArch': platform.machine(),
        'pythonVersion': platform.python_version(),
        'dumpTime': nowTime,
        'dumpTimeFormated': time.ctime(),
    })

    try:
        globalsFiltered.update({'arkLogs': Logger.log})
    except:
        pass
    
    for key in [
        "__author__",
        "__doc__",
        "__package__",
        "__spec__",
        "__annotations__",
        "__cached__",
        "_EMPTY",
        "4", # ?
        "lang_dict",

    ]: globalsFiltered.pop(key, None)

    filename = f"./dumps/dump_{int(nowTime)}.json"
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(globalsFiltered, f, indent=4, ensure_ascii=False)

    try:
        log('Starting Traceback window because a exception detected.', type=Logger.Type.WARN)
        for i in tracelist[:-1]:
            log(i, type=Logger.Type.ERROR)
        log(f"Dumped to {filename}")
    except:
        print('WARN: Starting Traceback window because a exception detected.')
        for i in tracelist[:-1]:
            print(f'FAIL: {i}')
        print(f"Dumped to {filename}")

    traceWin = maliang.Tk(size=(width, height),
                      title=f'ArkLauncher traceback window | {__version__}')

    traceWin.resizable(0, 0)
    traceWin.topmost(True)
    
    cv = maliang.Canvas(traceWin)
    cv.place(width=width, height=height)

    text_msg1 = maliang.Text(cv, (50, 50), fontsize=23, family='Consolas', weight='bold')
    text_msg2 = maliang.Text(cv, (50, 80), fontsize=17, family='Consolas')

    text_msg1.set('An error detected.')
    text_msg2.set('You can take an screenshot in this window, and send it to the author.')

    text_trace = maliang.Text(cv, (50, 130), fontsize=14)
    text_trace.set(''.join(traceback.format_exception(exception)))

    traceWin.center()
    traceWin.mainloop()


try:
    import time
    startLoadTime = time.time()

    # === Standard Library ===
    import ctypes
    import json
    import os
    import platform
    import sys
    import threading
    import traceback
    from datetime import datetime

    # === Third-Party Libraries ===
    import colorama
    import darkdetect
    from PIL import Image
    import maliang
    import maliang.animation
    import maliang.theme

    # === Internal Frameworks ===
    import Frameworks.Logger as Logger
    import Frameworks.Utils as Utils
    import Frameworks.Configuration.config as configLib
    import Frameworks.Notify as Notify

    log = Logger.output
    Logger.logLevel = 5

    # === Console Title ===
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        user32 = ctypes.windll.user32
        user32.SetWindowTextW(
            hwnd, f'ArkLauncher Console Interface - {__version__}, {__subversion__}.')
    except: # fallback
        sys.stdout.write(f"\033]0;{'ArkLauncher Console Interface - {__version__}, {__subversion__}.'}\007")
        sys.stdout.flush()

    # === Configuration ===
    WIDTH, HEIGHT = 500, 800

    configLib.loadConfig()
    config = configLib.config
    locale = config['language']

    # === Global Resources & Appearance ===
    images = {}
    ResPath = 'Resources'
    _FONTS = []
    _THEME = 'dark'
    _BORDER = config['border']
    _BACKGROUND = 'ChiesaBianca'
    _ANIMATIONFPS = 1000
    maliang.configs.Env.system = 'Windows10'
    maliang.theme.manager.set_color_mode('dark')
    devPageDisplayed = False

    # === Constants ===
    _EMPTY = ('', '', '')
    _SYSTEM = platform.system()
    _SYSREL = platform.release()
    _SYSVER = platform.version()

    def getRelFromAbs(x, y):
        return (x - root.winfo_x(), y - root.winfo_y())

    def focusWindow(*args):
        maliang.animation.MoveWindow(root, offset=(getRelFromAbs(root.winfo_screenwidth() - 515, root.winfo_y())), duration=500,
                                        controller=maliang.animation.controllers.ease_out, fps=_ANIMATIONFPS, end=lambda: root.geometry(position=(root.winfo_screenwidth() - 515, root.winfo_y()))).start()

    def minimizeAndExit():
        animation = maliang.animation.MoveWindow(root, offset=(root.winfo_screenwidth() - root.winfo_x(), (root.winfo_screenheight() // 2 - root.winfo_y() - 400)), duration=750, controller=maliang.animation.controllers.ease_out, fps=_ANIMATIONFPS)
        animation.end = lambda: (animation.stop(), root.destroy())
        animation.start()


    def testDragAndDrop(*args):
        log(f'dnd: {args}')


    def updateFont():
        global FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT, _FONTS

        for i in os.listdir(f'{ResPath}/font'):
            _FONTS = Utils.loadFont(f'{ResPath}/font/{i}', _FONTS)

        log(f'Loaded {len(os.listdir(f"{ResPath}/font"))} fonts.')

        FONT_FAMILY = 'Segoe UI'
        FONT_FAMILY_BOLD = f'Microsoft YaHei UI Bold'
        FONT_FAMILY_LIGHT = f'Microsoft YaHei UI Light'


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

        log(f'Loaded {len(image_paths["contributors"]) + len(image_paths["country"]) + len(image_paths[None])} images.')


    def getImage(target, category=None):
        try:
            if category:
                img = images[category][target]
            else:
                img = images[target]

            return img
        except:
            log(f'Image \"{target}\" is missing from category \"{category}\".',
                type=Logger.Type.WARN)
            return images['icon_unknown']


    def openGithub(name):
        os.system(f'start https://github.com/{name}')


    def createRoot(x=710, y=200):
        global root

        root = maliang.Tk(size=(WIDTH, HEIGHT), position=(-1000, -1000))  
        root.geometry(position=(root.winfo_screenwidth() - 15, root.winfo_screenheight() // 2 - 400))
        root.title(f'{translate("prodname")} {translate(__version__)}-{__subversion__}')
        root.minsize(WIDTH, HEIGHT)
        root.maxsize(WIDTH, HEIGHT)
        maliang.theme.manager.customize_window(root, disable_maximize_button=True, border_type=_BORDER)
        maliang.theme.apply_file_dnd(root, command=testDragAndDrop)    
        
        root.at_exit(minimizeAndExit, ensure_destroy=False)

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

        topImage            = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(Utils.makeImageBlur(backgroundImage.crop((0, 0, WIDTH, 65)), radius=10)))
        topMask             = maliang.Image(topBar, position=(0, 0), image=maliang.PhotoImage(Utils.makeImageMask(size=(WIDTH, 65))))
        topIconMask         = maliang.Image(topMask, position=(0, 0),image=maliang.PhotoImage(Utils.makeImageMask(size=(65, 65), color=(0, 0, 0, 16))))
        logo                = maliang.IconButton(topIconMask, size=(65, 65), position=(365, 2), image=maliang.PhotoImage(getImage('icon_logo').resize((40, 40), 1)))

        logo.style.set(bg=_EMPTY, ol=_EMPTY)
        

    close = None

    def updateTopBar(barType):
        global topMask, topImage, topSearchMask, topMask, logo, close
        upHEIGHT            = 65
        if barType == 'mainPage':
            if close:
                maliang.animation.MoveWidget(close, duration=350, fps=_ANIMATIONFPS, offset=(0, -65), controller=maliang.animation.ease_out).start()
            topSearchMask       = maliang.Image(topMask, position=(upHEIGHT, -65), image=maliang.PhotoImage(Utils.makeImageMask(size=(int(WIDTH - (upHEIGHT * 2)), upHEIGHT), color=(0, 0, 0, 50))))
            searchBox           = maliang.InputBox(topSearchMask, position=(0, 2), size=(int(WIDTH - (upHEIGHT * 3)), upHEIGHT - 4), placeholder=translate('search'), family=FONT_FAMILY_BOLD, fontsize=18)
            searchBox.style.set(bg=_EMPTY, ol=_EMPTY)

            avatar          = maliang.IconButton(topMask, size=(63, 63), position=(int(WIDTH - 65), 3), image=maliang.PhotoImage(Utils.makeImageRadius(getImage('icon_account'), 128, 0.7).resize((40, 40), 1)))
            avatar.style.set(bg=_EMPTY, ol=_EMPTY)
            maliang.animation.MoveWidget(logo, duration=350, fps=_ANIMATIONFPS, offset=(-365, 0), controller=maliang.animation.ease_out).start(delay=25)
            maliang.animation.MoveWidget(topSearchMask, duration=350, fps=_ANIMATIONFPS, offset=(0, 65), controller=maliang.animation.ease_out).start(delay=25)

        elif barType == 'welcomePage':
            pass
            
        else:
            if topSearchMask:
                maliang.animation.MoveWidget(topSearchMask, duration=350, fps=_ANIMATIONFPS, offset=(0, -65), controller=maliang.animation.ease_out).start(delay=25)
            upHEIGHT            = 65

            now = datetime.now()
            curTimeMonth        = maliang.Text(topMask, position=(85, 14), text=f'{now.strftime("%Y/%m/%d")}', family=FONT_FAMILY, fontsize=10)
            curTimeDay          = maliang.Text(topMask, position=(85, 23), text=f'{now.strftime("%H:%M")}', family=FONT_FAMILY_BOLD, fontsize=23)
            

            curTimeMonth.style.set(fg='#A5A9AC')

            maliang.animation.MoveWidget(logo, duration=350, fps=_ANIMATIONFPS, offset=(365, 0), controller=maliang.animation.ease_out).start(delay=25)
            close = maliang.IconButton(topIconMask, (2, -63), (upHEIGHT - 4, upHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_close').resize((40, 40), 1)), command=lambda: (curTimeMonth.destroy(), curTimeDay.destroy(), changeWindow(mainPage)))
            close.style.set(bg=('', '', ''), ol=(''))  
            maliang.animation.MoveWidget(close, duration=350, fps=_ANIMATIONFPS, offset=(0, 65), controller=maliang.animation.ease_out).start(delay=25)


    def changeWindow(window, extra_args = ()):
        log(f'Perform change canvas to "{window.__name__}"...', type=Logger.Type.INFO)
        root.after(1000, cv.destroy)
        try:
            Utils.play('change')
            updateTopBar(window.__name__)
            window(extra_args)
        except RuntimeError:
            log('Calling Tcl from tray thread.', type=Logger.Type.WARN)


    def loadLocale():
        global lang_dict

        lang_dict = {}

        for i in os.listdir(f'{ResPath}/lang'):
            if i.endswith('.json'):
                with open(f'{ResPath}/lang/{i}', encoding='utf-8') as f:
                    lang_dict[i[:-5]] = json.loads(f.read())

        log(f'Loaded {len(os.listdir(f"{ResPath}/lang"))} locales.')


    def translate(target):
        try:
            text = lang_dict[locale][target]
            return text
        except:
            log(f'String \"{target}\" missing in language \"{locale}\".',
                type=Logger.Type.WARN)
            return target


    def welcomePage():
        global locale, cv
        cv = createPage()

        backgroundImage = Utils.mergeImage(Utils.makeImageBlur(getImage(_BACKGROUND, 'background'), radius=25),
                                    Utils.makeImageMask((500, 800), (0, 0, 0, 64)))

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


    def mainPage(*_):
        global cv
        cv = createPage()
        cv.bind("<Escape>", lambda event: minimizeAndExit())


        backgroundImage = getImage(_BACKGROUND, 'background').crop((0, 65, WIDTH, HEIGHT))

        background = maliang.Image(cv, position=(0, 0), size=(
            WIDTH, HEIGHT), image=maliang.PhotoImage(backgroundImage))

        bottomHEIGHT        = 265
        bottomMaskHEIGHT    = 70
        bottomLMaskHEIGHT   = 130
        bottomImage         = maliang.Image(cv, position=(0, 535), image=maliang.PhotoImage(Utils.makeImageBlur(backgroundImage.crop((0, HEIGHT - bottomHEIGHT, WIDTH, HEIGHT)), radius=10)))
        bottomMask          = maliang.Image(cv, position=(0, 535), image=maliang.PhotoImage(Utils.makeImageMask(size=(HEIGHT, bottomHEIGHT))))
        bottomSettingsMask  = maliang.Image(bottomMask, position=(bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=maliang.PhotoImage(Utils.makeImageRadius(Utils.makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
        bottomAccountMask   = maliang.Image(bottomMask, position=(500 - bottomMaskHEIGHT // 2, bottomMaskHEIGHT // 2), image=maliang.PhotoImage(Utils.makeImageRadius(Utils.makeImageMask(size=(bottomMaskHEIGHT, bottomMaskHEIGHT), color=(0, 0, 0, 128)), bottomMaskHEIGHT, alpha=0.1).resize((50, 50), 1)), anchor='center')
        bottomSubMask       = maliang.Image(bottomMask, position=(0, bottomMaskHEIGHT), image=maliang.PhotoImage(Utils.makeImageMask((WIDTH, bottomLMaskHEIGHT), color=(0, 0, 0, 64))))
        bottomLaunchMask    = maliang.Image(bottomSubMask, position=(10, 7), image=maliang.PhotoImage(Utils.makeImageMask((480, 116), color=(0, 0, 0, 64))))

        settings            = maliang.IconButton(bottomSettingsMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_settings').resize((40, 40), 1)), command=lambda: changeWindow(settingsPage, extra_args=(4)), anchor='center')
        account             = maliang.IconButton(bottomAccountMask, (0, 0), (bottomMaskHEIGHT - 4, bottomMaskHEIGHT - 4), image=maliang.PhotoImage(getImage('icon_account').resize((40, 40), 1)), command=lambda: changeWindow(settingsPage, extra_args=(0)), anchor='center')

        launch              = maliang.Button(bottomLaunchMask, (0, 0), size=(480, 116), command=lambda: Notify.toast(title='testTitle', message='testMessage', duration=2000, root=root, icon=getImage('icon_logo').resize((60, 60), 1)))
        launchIcon          = maliang.Image(launch, (bottomLMaskHEIGHT // 2 - 5, bottomLMaskHEIGHT // 2 - 7),image=maliang.PhotoImage(getImage('icon_launch').resize((80, 80), 1)), anchor='center')
        launchDesc          = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 35), text='Launch game', family=FONT_FAMILY,fontsize=17)
        launchTitle         = maliang.Text(launch, position=(105, bottomLMaskHEIGHT // 2 - 10), text='Meira Client', family=FONT_FAMILY_BOLD, fontsize=25)

        if __version__ == 'dev':
            global devPageDisplayed            
            
            if not devPageDisplayed:
                Utils.play('invite')
                devWin = maliang.Label(cv, position=(40, 40), size=(420, 600))
                maliang.animation.MoveWidget(devWin, offset=(0, 1000), duration=0).start()
                maliang.animation.MoveWidget(devWin, offset=(0, -1000), duration=500, controller=maliang.animation.ease_out, fps=_ANIMATIONFPS).start()
                dev_Icon            = maliang.Image(devWin, position=(30, 40), image=maliang.PhotoImage(getImage('icon_logo').resize((50, 50), 1)))
                dev_welcome         = maliang.Text(devWin, position=(40, 110), fontsize=20, family=FONT_FAMILY_BOLD, text=translate('dev_welcome'))

                dev_text1         = maliang.Text(devWin, position=(40, 170), fontsize=15, family=FONT_FAMILY, text=translate('dev_text1'))
                dev_text2         = maliang.Text(devWin, position=(40, 220), fontsize=15, family=FONT_FAMILY, text=translate('dev_text2'))
                dev_text3         = maliang.Text(devWin, position=(40, 290), fontsize=15, family=FONT_FAMILY, text=translate('dev_text3'))

                dev_btn           = maliang.Button(devWin, position=(210, 550), size=(350, 50), anchor='center', text='OK', fontsize=18, family=FONT_FAMILY_BOLD, command=lambda: (Utils.play('launch'), maliang.animation.MoveWidget(devWin, offset=(0, -1000), duration=1000, controller=maliang.animation.ease_out, end=devWin.destroy, fps=_ANIMATIONFPS).start()))

                devWin.style.set(bg=('#202020', '#202020'))
            devPageDisplayed = True

        launch.style.set(fg=('', '', ''), bg=('', '', ''), ol=('#4C4849', '#BBBBBB'))
        account.style.set(bg=_EMPTY, ol=_EMPTY)
        settings.style.set(bg=_EMPTY, ol=_EMPTY)

        # logo.bind("<B1-Motion>", on_drag_motion)


        root.mainloop()


    def settingsPage(default = 4):
        global cv

        currentPage = 0

        cv = createPage()
        cv.bind("<Escape>", lambda event: changeWindow(mainPage))

        backgroundImage = Utils.mergeImage(Utils.makeImageBlur(getImage(_BACKGROUND, 'background'), radius=25),
                                Utils.makeImageMask((500, 800), (0, 0, 0, 64)))

        def createSubPage(i, oldcv):
            subcv = maliang.Canvas(cv)
            if i > currentPage:
                x = 500
            elif i < currentPage:
                x = -500
            else:
                x = 0
            subcv.place(x=x, y=50, width=WIDTH, height=800-50)
            maliang.Image(subcv, position=(0, -50), size=(500, 800), image=maliang.PhotoImage(backgroundImage))

            if oldcv:
                maliang.animation.MoveTkWidget(
                    oldcv,
                    offset=(0 - x, 0),
                    duration=400,
                    controller=maliang.animation.ease_out,
                    fps=_ANIMATIONFPS,  
                    end=oldcv.destroy
                ).start(delay=1)

                maliang.animation.MoveTkWidget(
                    subcv,
                    offset=(0 - x, 0),
                    duration=400,
                    controller=maliang.animation.ease_out,
                    fps=_ANIMATIONFPS
                ).start()


            else:
                maliang.animation.MoveTkWidget(
                    subcv,
                    offset=(0 - x, 0),
                    duration=500,
                    controller=maliang.animation.ease_out,
                    fps=_ANIMATIONFPS
                ).start()

            return subcv



        
        def pageAbout():
            smoke = Utils.makeImageRadius(Utils.makeImageMask((500, 800)), radius=5)
            maliang.Image(subcv, position=(0, 0), size=(500, 800), image=maliang.PhotoImage(smoke))
            maliang.Image(subcv, position=(50, 50), image=maliang.PhotoImage(getImage('icon_logo').resize((100, 100), 1)))

            maliang.Text(subcv, position=(60, 180), text=translate('parent'), family=FONT_FAMILY, fontsize=20)
            maliang.Text(subcv, position=(60, 207), text=translate('prodname'), family=FONT_FAMILY_BOLD, fontsize=32)
            maliang.Text(subcv, position=(60, 250), text=f"{translate('version')}: {__version__}-{__subversion__}", family=FONT_FAMILY, fontsize=16)
            
            maliang.Text(subcv, position=(60, 300), text=translate('license'), family=FONT_FAMILY, fontsize=16)

        def pageLanguage():
            container = maliang.Label(subcv, position=(40, 40), size=(420, 600))
            container.style.set(bg=('#00000000', '#00000000'), ol=('#00000000', '#00000000'))

            smoke = Utils.makeImageRadius(Utils.makeImageMask(container.size), radius=5)
            maliang.Image(subcv, position=container.position, size=container.size, image=maliang.PhotoImage(smoke))
            container.destroy()
            

        maliang.Image(cv, position=(0, 0), size=(500, 800), image=maliang.PhotoImage(backgroundImage))
        optionsMask          = maliang.Image(cv, position=(0, 0), size=(500, 50), image=maliang.PhotoImage(Utils.makeImageMask(size=(500, 50), color=(0, 0, 0, 80))))

        subcv = None
        def handler(i):
            nonlocal subcv, currentPage

            subcv = createSubPage(i, subcv)
            currentPage = i
            if i == 1:
                pageLanguage()
            if i == 4:
                pageAbout()

        options = maliang.SegmentedButton(optionsMask, position=(250, 25), family=FONT_FAMILY_BOLD, fontsize=16, command=lambda i: (Utils.play('change'), handler(i)), anchor='center', default=default, text=[translate('account'), translate('locale'), translate('network'), translate('customize'), translate('about')])
        options.style.set(bg=('', ''), ol=('', ''))
        for i in options.children:
            i.style.set(fg=('#888888', '#AAAAAA', '#CCCCCC', '#FFFFFF'), bg=('', '', '', '', '', ''), ol=('', '', '', '', '', ''))

        handler(default)

        root.mainloop()

    # === Initialization ===
    log(f'System: {_SYSTEM} {_SYSREL} ({_SYSVER})')

    colorama.init()

    refreshImage(threaded=False)

    # icon = Tray.Icon("name", getImage('icon_logo'), "ArkLauncher Tray", menu=[
    #     Tray.MenuItem("Exit", minimizeAndExit, default=True)
    # ])

    # threading.Thread(target=icon.run, daemon=True).start()

    # === Load UI ===
    loadLocale()
    updateFont() 
    createRoot()
    createTopBar()
    focusWindow()

    endLoadTime = int((time.time() - startLoadTime) * 1000)

    log(f'Loaded ArkLauncher in {endLoadTime} ms.')
    log(f'Welcome to Ark!')

    if configLib.first:
        updateTopBar('welcomePage')
        welcomePage()
    else:
        updateTopBar('mainPage')
        mainPage()

except Exception as f:
    tracebackWindow(f)


