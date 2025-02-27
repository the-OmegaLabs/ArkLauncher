from pyglet.resource import animation

_VERSION = 'dev'
_SUBVERSION = '25w09f'

import json
import os
import platform
import threading
import traceback
if platform.system() == 'Windows':
    import win32material
from datetime import datetime
if platform.system() == 'Windows':
    from ctypes import windll, c_char_p

import colorama
import darkdetect
import maliang
import maliang.animation
import maliang.core
import maliang.theme
from PIL import Image

import ark
import libs.config as configLib
from libs import olog as olog
from libs.olog import output as log

WIDTH = 500
HEIGHT = 800

configLib.loadConfig()
config = configLib.config
locale = config['language']
_THEME = config['theme']
_BORDER = config['border']
_WINDOW_STYLE = config['style']
maliang.theme.manager.set_color_mode(_THEME)

if _THEME in ('system', 'auto'):
    _THEME = darkdetect.theme().lower()

if platform.system() == 'Windows':
    import libs.avatar.Windows as avatar

    FONT_FAMILY = 'Microsoft YaHei UI'
    FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
    FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'
elif platform.system() == 'Linux':
    import libs.avatar.Linux as avatar

    FONT_FAMILY = 'Noto Sans'
    FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
    FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'

olog.logLevel = 5

log(f'Starting ArkLauncher GUI, version {_VERSION}-{_SUBVERSION}.')

if platform.system() == 'Windows':
    import libs.avatar.Windows as avatar
elif platform.system() == 'Linux':
    import libs.avatar.Linux as avatar

colorama.init()

images = {}


def refreshImage():
    global images

    def loadImage(path):
        try:
            img = Image.open(path)
            return img
        except Exception as e:
            print(f"Error loading image {path}: {e}")
            return None

    def threadedImageOpen(path, dict_key, category=None):
        """Threaded image loading function with category support."""
        img = loadImage(path)
        if img:
            if category:
                if category not in images:
                    images[category] = {}
                images[category][dict_key] = img
            else:
                images[dict_key] = img
            log(f"Loaded image: {path}", type=olog.Type.DEBUG)

    theme = darkdetect.theme().lower() if _THEME == 'system' else _THEME

    # Initialize images dictionary with categories
    images = {
        'contributors': {},
        'country': {}
    }

    # Define image paths with categories
    image_paths = {
        'contributors': {
            'maliang': 'src/Contributors/maliang.png',
            'Stevesuk0': 'src/Contributors/Stevesuk0.jpg',
            'bzym2': 'src/Contributors/bzym2.png',
            'HRGC-Sonrai': 'src/Contributors/HRGC-Sonrai.jpg',
            'Xiaokang2022': 'src/Contributors/Xiaokang2022.jpg',
            'the-OmegaLabs': 'src/Contributors/the-OmegaLabs.png',
        },
        'country': {
            'cn': 'src/both/country_cn.png',
            'jp': 'src/both/country_jp.png',
            'ko': 'src/both/country_ko.png',
            'en': 'src/both/country_us.png',
            'sb': 'src/both/transgender.png',
        },
        None: {  # Regular images without category
            'avatar': avatar.getAvatar(),
            'icon_quick': 'src/both/quick.png',
            'icon_logo': 'src/icon.png',
            'icon_return': f'src/{theme}/return.png',
            'icon_settings': f'src/{theme}/settings.png',
            'icon_about': f'src/{theme}/about.png',
            'icon_language': f'src/{theme}/language.png',
            'icon_network': f'src/{theme}/network.png',
            'icon_account': f'src/{theme}/account.png',
            'icon_customize': f'src/{theme}/customize.png',
            'icon_dark': f'src/{theme}/dark.png',
            'icon_light': f'src/{theme}/light.png',
            'icon_auto': f'src/{theme}/auto.png'
        }
    }

    # Load all images with their respective categories
    for category, items in image_paths.items():
        for key, path in items.items():
            threading.Thread(
                target=threadedImageOpen,
                args=(path, key, category)
            ).start()


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
    if platform.system() == 'Windows':
        hwid = windll.user32.FindWindowW(c_char_p(None), f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')
    root.icon(maliang.PhotoImage(images['icon_logo'].resize((32, 32), 1)))
    return root, cv


def changeWindow(window, root: maliang.Tk):
    log(f'Perform change window to "{window.__name__}"...', type=olog.Type.INFO)
    x, y = root.winfo_x(), root.winfo_y()
    if platform.system() == 'Linux':
        x -= 5
        y -= 31
    root.destroy()
    window(x, y)


def welcomePage():
    global locale
    root, cv = createWindow()

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
        lang = lang_dict.get(lang_key, lang_dict['en'])
        locale = lang_key

        text_welcome.set(translate('welcome'))
        text_desc.set(translate('desc'))
        text_license.set(translate('license'))
        text_collect.set(translate('collect'))
        text_button_chinese.set(translate('lang_chinese'))
        button.set(translate('button'))

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
        noticeSubText = maliang.Text(noticeBar, (65, 36), text=sub, family=FONT_FAMILY, fontsize=14)

        if spin == True:
            noticeSpinner = maliang.Spinner(noticeBar, (35, 35), mode="indeterminate", anchor='center')
            return [noticeBar, noticeText, noticeSpinner]
        else:
            return [noticeBar, noticeText]

    def playToastAnimation(notice: maliang.Label):
        animation = maliang.animation.MoveWidget(notice, offset=(0, -100), duration=500,
                                                 controller=maliang.animation.ease_out, fps=500)
        animation.start()

    subtitle, title = (None, None)

    icon_x = 50
    icon_y = 40
    icon_size = 60
    logo_icon = maliang.Image(cv, (icon_x, icon_y),
                              image=maliang.PhotoImage(images['icon_logo'].resize((icon_size, icon_size), 1)))

    greeting_text = maliang.Text(cv, (58, icon_y + icon_size + 7),
                                 family=FONT_FAMILY_BOLD,
                                 fontsize=24)

    greeting_text.set(getTimeBasedGreeting())

    content_start_y = 165

    button_new = maliang.Button(cv, position=(50, content_start_y), size=(400, 100))
    maliang.Text(button_new, (200, 50), text='+', family=FONT_FAMILY_BOLD, fontsize=50, anchor='center')

    maliang.Tooltip(
        maliang.IconButton(cv, position=(400, 50), size=(50, 50),
                           command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(images['icon_settings'].resize((55, 55), 1))),
        text=translate('settings'), fontsize=13)

    maliang.Tooltip(
        maliang.IconButton(cv, position=(340, 50), size=(50, 50),
                           command=lambda: changeWindow(mainPage, root),
                           image=maliang.PhotoImage(images['icon_quick'].resize((40, 40), 1))),
        text=translate('quick'),
        fontsize=13)

    noticeBar, _, _ = createNotice(f"{translate('logging_in')} {translate('parent')}...",
                                   translate('wait'), cv, 1)

    playToastAnimation(noticeBar)
    root.mainloop()


def settingsPage(x, y):
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['avatar'].resize((45, 45), 1)))

    HEIGHT = 165
    button_account = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                        command=lambda: changeWindow(settingsAccountPage, root),
                                        image=maliang.PhotoImage(images['icon_account'].resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 65
    button_language = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                         command=lambda: changeWindow(settingsLanguagePage, root),
                                         image=maliang.PhotoImage(images['icon_language'].resize((40, 40), 1)),
                                         family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 65
    button_network = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                        command=lambda: changeWindow(settingsNetworkPage, root),
                                        image=maliang.PhotoImage(images['icon_network'].resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    HEIGHT += 65
    button_customize = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                          command=lambda: changeWindow(settingsCustomizePage, root),
                                          image=maliang.PhotoImage(images['icon_customize'].resize((40, 40), 1)),
                                          family=FONT_FAMILY_BOLD,
                                          fontsize=18)
    HEIGHT += 65
    button_about = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
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
    buttons = [
        None,
        None,
        None,
        None,
        None
    ]

    def handleInput(url: maliang.InputBox, button: maliang.Label, confirm: maliang.Button):
        boxinput = url.get()
        if not boxinput:
            button.destroy()
            index = buttons.index(button)
            buttons.pop(index)
            buttons.insert(index, None)
            log(f'Buttons: {buttons}', type=olog.Type.DEBUG)
        else:
            confirm.destroy()
            url.disable()

            confirm = maliang.Spinner(button, size=(35, 35), position=(330, 33), mode='indeterminate')

            if boxinput.startswith('https://') or boxinput.startswith('http://'):
                response = ark.getSourceContent(boxinput)
                if response[0]:
                    url.destroy()
                    confirm.destroy()

                    logo = maliang.Image(button, (25, 20), size=(60, 60),
                                         image=maliang.PhotoImage(response[1]['icon'].resize((50, 50), 1)))
                    motd = maliang.Text(button, (100, 23), family=FONT_FAMILY, fontsize=22)
                    motd.set(response[1]['name'])
                    desc = maliang.Text(button, (100, 55), family=FONT_FAMILY_LIGHT, fontsize=16)
                    desc.set(f"{response[1]['type']} · {boxinput.split('/')[2].split('/')[0]}")

    def createSource():
        nonlocal button_new, buttons, cv

        index = buttons.index(None)
        HEIGHT = 165 + 110 * index
        button = maliang.Label(cv, position=(50, HEIGHT), size=(400, 100))
        url = maliang.InputBox(button, position=(25, 25), placeholder="URL", size=(290, 50), fontsize=16)
        url.set('http://127.0.0.1:8000/')
        confirm = maliang.Button(button, size=(50, 50), position=(325, 25), fontsize=35, text='+',
                                 family=FONT_FAMILY_BOLD)
        confirm.bind('<Button-1>', lambda event: handleInput(url, button, confirm))
        url.bind('<Return>', lambda event: handleInput(url, button, confirm))

        buttons[index] = button
        log(f'Buttons: {buttons}', type=olog.Type.DEBUG)

    button_new = maliang.Button(cv, position=(400, 50), size=(50, 50), command=createSource)
    maliang.Text(button_new, (25, 22), text='+', family=FONT_FAMILY, fontsize=50, anchor='center')

    root.mainloop()


def settingsCustomizePage(x, y):
    global _THEME
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('customize'))

    def changeTheme(theme):
        global _THEME

        _THEME = theme
        configLib.setConfig('theme', _THEME)
        configLib.sync()

        if _THEME == 'system':
            _THEME = darkdetect.theme().lower()

        log(f"Changing window to {_THEME} style.", type=olog.Type.INFO)
        refreshImage()
        maliang.theme.manager.set_color_mode(_THEME)
        maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

        HEIGHT = 165
        buttonDark = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55), command=lambda: changeTheme('dark'),
                                        family=FONT_FAMILY_BOLD,
                                        image=maliang.PhotoImage(images['icon_dark'].resize((40, 40), 1)), fontsize=18)
        HEIGHT += 65
        buttonLight = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                         command=lambda: changeTheme('light'), family=FONT_FAMILY_BOLD,
                                         image=maliang.PhotoImage(images['icon_light'].resize((40, 40), 1)),
                                         fontsize=18)
        HEIGHT += 65
        buttonSystem = maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55),
                                          command=lambda: changeTheme('system'), family=FONT_FAMILY_BOLD,
                                          image=maliang.PhotoImage(images['icon_auto'].resize((40, 40), 1)),
                                          fontsize=18)
        log(f"Instant change widget to {_THEME} style.", type=olog.Type.DEBUG)

        buttonDark.set(translate('dark'))
        buttonLight.set(translate('light'))
        buttonSystem.set(translate('auto'))

    changeTheme(_THEME)

    root.mainloop()


def loadLocale():
    global lang_dict

    lang_dict = {}

    for i in os.listdir('./src/lang'):
        if i.endswith('.json'):
            log(f'Loading locale file "{i}"...')
            with open(f'./src/lang/{i}', encoding='utf-8') as f:
                lang_dict[i[:-5]] = json.loads(f.read())


def translate(target):
    return lang_dict.get(locale, {}).get(target, lang_dict['en'].get(target, target))


def settingsLanguagePage(x, y):
    global locale, FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT
    root, cv = createWindow(x, y)

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(images['icon_return'].resize((55, 55), 1)))

    def setLanguage(language, root: maliang.Tk):
        global FONT_FAMILY, FONT_FAMILY_BOLD, FONT_FAMILY_LIGHT, locale
        log(f'Change locale to {language}.')

        if language == 'jp':
            FONT_FAMILY = 'Yu Gothic UI'
            FONT_FAMILY_BOLD = f'Yu Gothic UI Bold'
            FONT_FAMILY_LIGHT = f'Yu Gothic UI Light'
        elif language in ('cn'):
            FONT_FAMILY = 'Microsoft YaHei UI'
            FONT_FAMILY_BOLD = f'Microsoft YaHei UI Bold'
            FONT_FAMILY_LIGHT = f'Microsoft YaHei UI Light'
        elif language in ('sb'):
            FONT_FAMILY = 'Simsun'
            FONT_FAMILY_BOLD = f'Simhei'
            FONT_FAMILY_LIGHT = f'FangSong'
        elif language in ('ko'):
            FONT_FAMILY = 'Malgun Gothic'
            FONT_FAMILY_BOLD = f'Malgun Gothic Bold'
            FONT_FAMILY_LIGHT = f'Malgun Gothic'
        else:
            FONT_FAMILY = 'Segoe UI'
            FONT_FAMILY_BOLD = f'Segoe UI Semibold'
            FONT_FAMILY_LIGHT = f'Segoe UI Light'

        log(f'Change font to {FONT_FAMILY}', type=olog.Type.DEBUG)

        locale = language
        configLib.setConfig('language', locale)
        configLib.sync()

        HEIGHT = 165
        lang_changebutton = []

        if 'country' in images:
            for i in lang_dict:
                if i in images['country']:
                    lang_changebutton.append(
                        maliang.IconButton(
                            cv,
                            position=(50, HEIGHT),
                            size=(400, 55),
                            command=lambda lang=i: setLanguage(lang, root),
                            image=maliang.PhotoImage(images['country'][i].resize((40, 40), 1)),
                            family=FONT_FAMILY_BOLD,
                            fontsize=18
                        )
                    )
                    HEIGHT += 65

        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))

        tmp = [f'setlang_{i}' for i in lang_dict]
        for i in range(len(lang_changebutton)):
            lang_changebutton[i].set(translate(tmp[i]))

        root.title(f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')

    setLanguage(locale, root)
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
    loadLocale()
    refreshImage()

    if configLib.first:
        welcomePage()
    else:
        mainPage(710, 200)

except Exception as f:
    tracebackWindow(f)
