import json
import os
import colorama
import darkdetect
import platform
import maliang
import maliang.core
import maliang.theme
import traceback
from PIL import Image

from libs.olog import output as log
from libs.olog import WARN, ERROR, INFO, DEBUG

colorama.init()

_VERSION = ''
_SUBVERSION = ''
_THEME = darkdetect.theme().lower()
WIDTH = 500
HEIGHT = 900

FONT_FAMILY = 'Microsoft YaHei UI'
FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
FONT_FAMILY_LIGHT = f'{FONT_FAMILY} Light'

if platform.system() == 'Windows':
    import libs.winavatar as avatar
else:
    import libs.linavatar as avatar


def openGithub(name):
    os.system(f'start https://github.com/{name}')

def createWindow(x=None, y=None):
    log(f'Creating new page at ({x}, {y}).', type=DEBUG)
    icon = Image.open('src/icon.png')
    if x and y:
        root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')
    else:
        root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')
    
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32), 1)))
    return root, cv


def changeWindow(window, root: maliang.Tk):
    log(f'Perform change window to "{window.__name__}"...', type=INFO)
    x, y = root.winfo_x(), root.winfo_y()
    if platform.system() == 'Linux':
        x -= 5
        y -= 31
    root.destroy()
    window(x, y)


def welcomePage():
    global locale
    root, cv = createWindow()

    icon = Image.open('src/icon.png')

    maliang.Image(cv, (50, 75), image=maliang.PhotoImage(icon.resize((150, 150), 1)))
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

    # 切换到英文
    def changeToEnglish(_):
        changeLanguage('en')

    # 处理按下 shift 键时的彩蛋语言
    def changeToChinese(_):
        changeLanguage('cn')

    maliang.CheckBox(cv, (50, 600), command=agreeLicense, default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    # 初始化时使用中文
    changeLanguage('cn')

    root.mainloop()


def aboutPage(x, y):
    # Create main window
    root, cv = createWindow(x, y)
    
    # Load all required images
    images = {
        'return': Image.open(f'src/{_THEME}/return.png'),
        'icon': Image.open('src/icon.png'),
        'contributors': {
            'maliang': Image.open(f'src/Contributors/maliang.png'),
            'Stevesuk0': Image.open(f'src/Contributors/Stevesuk0.jpg'),
            'bzym2': Image.open(f'src/Contributors/bzym2.png'),
            'HRGC_Sonrai': Image.open(f'src/Contributors/HRGC-Sonrai.jpg'),
            'Xiaokang2022': Image.open(f'src/Contributors/Xiaokang2022.jpg'),
            'theOmegaLabs': Image.open(f'src/Contributors/the-OmegaLabs.png')
        }
    }
    
    # Calculate center point
    center_x = x // 2
    
    # Header section
    maliang.IconButton(
        cv, 
        position=(40, 40),
        size=(50, 50),
        command=lambda: changeWindow(settingsPage, root),
        image=maliang.PhotoImage(images['return'].resize((55, 55), 1))
    )
    
    # Title texts
    maliang.Text(cv, (100, 40), text=translate("settings"), family=FONT_FAMILY_LIGHT, fontsize=15)
    maliang.Text(cv, (100, 60), text=translate("about"), family=FONT_FAMILY_BOLD, fontsize=26)
    
    # Project information section - Centered layout
    icon_size = 120
    icon_x = center_x - (icon_size // 2)
    
    # Large centered icon
    maliang.IconButton(
        cv,
        position=(icon_x, 120),
        size=(icon_size, icon_size),
        image=maliang.PhotoImage(images['icon'].resize((icon_size, icon_size))),
        command=lambda: openGithub('the-OmegaLabs/ArkLauncher')
    )
    
    # Center-aligned product information
    maliang.Text(
        cv, 
        (center_x, 270), 
        text="ATNetwork", 
        family=FONT_FAMILY_LIGHT, 
        fontsize=20,
        anchor='center'
    )
    maliang.Text(
        cv, 
        (center_x, 300), 
        text="ARKLauncher", 
        family=FONT_FAMILY_BOLD, 
        fontsize=32,
        anchor='center'
    )
    maliang.Text(
        cv, 
        (center_x, 330),
        text=f"Version: {translate(_VERSION)}-{_SUBVERSION}", 
        family=FONT_FAMILY, 
        fontsize=15,
        anchor='center'
    )
    
    # Contributors section - Centered title
    maliang.Text(
        cv, 
        (center_x, 400), 
        text=translate("contributors"), 
        family=FONT_FAMILY_BOLD, 
        fontsize=26,
        anchor='center'
    )
    
    # Contributors avatars - Centered as a group
    avatar_size = 50
    avatar_spacing = 70  # Space between avatars
    contributors = ['Stevesuk0', 'bzym2', 'HRGC_Sonrai']
    total_width = (len(contributors) - 1) * avatar_spacing + avatar_size
    
    start_x = center_x - (total_width // 2)
    
    for i, contributor in enumerate(contributors):
        x_pos = start_x + (i * avatar_spacing)
        maliang.IconButton(
            cv,
            position=(x_pos, 450),
            size=(avatar_size, avatar_size),
            command=lambda c=contributor: openGithub(c),
            image=maliang.PhotoImage(images['contributors'][contributor].resize((47, 47), 1))
        )
    
    # Special thanks section - Centered title
    maliang.Text(
        cv, 
        (center_x, 520), 
        text=translate("specialthanks"), 
        family=FONT_FAMILY_BOLD, 
        fontsize=26,
        anchor='center'
    )
    
    # Special thanks entries - Content blocks centered
    content_width = 300  # Approximate width of content blocks
    content_left = center_x - (content_width // 2)
    
    # Maliang
    maliang.IconButton(
        cv,
        position=(content_left, 570),
        size=(50, 50),
        command=lambda: openGithub('Xiaokang2022/maliang'),
        image=maliang.PhotoImage(images['contributors']['maliang'].resize((35, 35), 1))
    )
    maliang.Text(cv, (content_left + 65, 570), text='maliang', family=FONT_FAMILY_BOLD, fontsize=25)
    maliang.Text(cv, (content_left + 65, 602), text='A lightweight UI framework for python.', family=FONT_FAMILY, fontsize=15)
    
    # Zhikang Yan
    maliang.IconButton(
        cv,
        position=(content_left, 640),
        size=(50, 50),
        command=lambda: openGithub('Xiaokang2022'),
        image=maliang.PhotoImage(images['contributors']['Xiaokang2022'].resize((47, 47), 1))
    )
    maliang.Text(cv, (content_left + 65, 640), text='Zhikang Yan', family=FONT_FAMILY_BOLD, fontsize=25)
    maliang.Text(cv, (content_left + 65, 672), text="Developer of 'maliang'", family=FONT_FAMILY, fontsize=15)
    
    # Omega Labs
    maliang.IconButton(
        cv,
        position=(content_left, 710),
        size=(50, 50),
        command=lambda: openGithub('the-OmegaLabs'),
        image=maliang.PhotoImage(images['contributors']['theOmegaLabs'].resize((47, 47), 1))
    )
    maliang.Text(cv, (content_left + 65, 710), text='Omega Labs', family=FONT_FAMILY_BOLD, fontsize=25)
    maliang.Text(
        cv, 
        (content_left + 65, 742), 
        text='Developing a next-generation Linux ecosystem.', 
        family=FONT_FAMILY, 
        fontsize=15
    )
    
    root.mainloop()

def mainPage(x, y):
    root, cv = createWindow(x, y)

    def createNotice(str, cv, color):
        noticeBar = maliang.Canvas(master=cv, auto_update=False, bg=color)
        noticeBar.place(width=500, height=30, x=0, y=0)
        
        noticeText = maliang.Text(noticeBar, (250, 15), text=str, family=FONT_FAMILY_BOLD, anchor='center', fontsize=14, )

        return [noticeBar, noticeText]


    icon = Image.open('src/icon.png')
    icon_about = Image.open(f'src/{_THEME}/about.png')
    icon_settings = Image.open(f'src/{_THEME}/settings.png')
    icon_quick = Image.open(f'src/{_THEME}/quick.png')
    icon_testGame = Image.open(f'src/project/candee.png')

    maliang.Image(cv, (50, 50), image=maliang.PhotoImage(icon.resize((50, 50), 1)))
    maliang.Text(cv, (110, 50), text=translate('parent'), family=FONT_FAMILY, fontsize=15)
    maliang.Text(cv, (110, 68), text=translate('prodname'), family=FONT_FAMILY_BOLD, fontsize=26)

    button_new = maliang.Button(cv, position=(50, 130), size=(400, 100))
    maliang.Text(button_new, (200, 50), text='+', family=FONT_FAMILY_BOLD, fontsize=50, anchor='center')
    maliang.Tooltip(
        maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_settings.resize((55, 55), 1))), text=translate('settings'), fontsize=13)
    maliang.Tooltip(
        maliang.IconButton(cv, position=(340, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root),
                           image=maliang.PhotoImage(icon_quick.resize((40, 40), 1))), text=translate('quick'), fontsize=13)

    # noticeBar, _ = createNotice('正在登录到 ATNetwork...', cv, '#4D8DFA')
    # animation.MoveTkWidget(noticeBar, (600, 0), 1000, fps=1000, controller=animation.ease_out).start(delay=500)

    root.mainloop()


def settingsPage(x, y):
    print(FONT_FAMILY)
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{_THEME}/return.png')
    icon_about = Image.open(f'src/{_THEME}/about.png')
    icon_language = Image.open(f'src/{_THEME}/language.png')
    icon_network = Image.open(f'src/{_THEME}/network.png')
    icon_avatar = Image.open(avatar.getAvatar())
    icon_account = Image.open(f'src/{_THEME}/account.png')
    icon_customize = Image.open(f'src/{_THEME}/customize.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY_LIGHT, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                       image=maliang.PhotoImage(icon_avatar.resize((45, 45), 1)))

    button_account = maliang.IconButton(cv, position=(50, 150), size=(400, 55),
                                        command=lambda: changeWindow(settingsAccountPage, root),
                                        image=maliang.PhotoImage(icon_account.resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    button_language = maliang.IconButton(cv, position=(50, 210), size=(400, 55),
                                         command=lambda: changeWindow(settingsLanguagePage, root),
                                         image=maliang.PhotoImage(icon_language.resize((40, 40), 1)),
                                         family=FONT_FAMILY_BOLD, fontsize=18)
    button_network = maliang.IconButton(cv, position=(50, 270), size=(400, 55),
                                        command=lambda: changeWindow(settingsNetworkPage, root),
                                        image=maliang.PhotoImage(icon_network.resize((40, 40), 1)),
                                        family=FONT_FAMILY_BOLD, fontsize=18)
    button_customize = maliang.IconButton(cv, position=(50, 330), size=(400, 55),
                                          command=lambda: changeWindow(settingsCustomizePage, root),
                                          image=maliang.PhotoImage(icon_customize.resize((40, 40), 1)),
                                          family=FONT_FAMILY_BOLD,
                                          fontsize=18)
    button_about = maliang.IconButton(cv, position=(50, 390), size=(400, 55),
                                      command=lambda: changeWindow(aboutPage, root),
                                      image=maliang.PhotoImage(icon_about.resize((40, 40), 1)), family=FONT_FAMILY_BOLD,
                                      fontsize=18)


    text_logo1.set(translate('homepage'))
    text_logo2.set(translate('settings'))
    button_account.set(f" {translate('account')}")
    button_language.set(f" {translate('locale')}")
    button_network.set(f" {translate('network')}")
    button_about.set(f" {translate('about')}")
    button_customize.set(f" {translate('customize')}")

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    root.mainloop()


def settingsAccountPage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{_THEME}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('account'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    root.mainloop()


def settingsNetworkPage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{_THEME}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('network'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

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

        if _THEME == 'system':
            _THEME = darkdetect.theme().lower()

        log(f"Changing window to {_THEME} style.", type=INFO)

        maliang.theme.manager.set_color_mode(_THEME)
        icon_return = Image.open(f'src/{_THEME}/return.png')
        icon_dark = Image.open(f'src/{_THEME}/dark.png')
        icon_light = Image.open(f'src/{_THEME}/light.png')
        icon_auto = Image.open(f'src/{_THEME}/auto.png')

        maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                            image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

        buttonDark = maliang.IconButton(cv, position=(50, 150), size=(400, 55), command=lambda: changeTheme('dark'), family=FONT_FAMILY_BOLD,
                                image=maliang.PhotoImage(icon_dark.resize((40, 40), 1)), fontsize=18)
        buttonLight = maliang.IconButton(cv, position=(50, 210), size=(400, 55), command=lambda: changeTheme('light'), family=FONT_FAMILY_BOLD,
                                image=maliang.PhotoImage(icon_light.resize((40, 40), 1)), fontsize=18)
        buttonSystem = maliang.IconButton(cv, position=(50, 270), size=(400, 55), command=lambda: changeTheme('system'), family=FONT_FAMILY_BOLD,
                                image=maliang.PhotoImage(icon_auto.resize((40, 40), 1)), fontsize=18)
        log(f"Instant change widget to {_THEME} style.", type=DEBUG)

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
    global locale, FONT_FAMILY, FONT_FAMILY_BOLD
    root, cv = createWindow(x, y)

    icon_language = Image.open(f'src/{_THEME}/language.png')
    icon_return = Image.open(f'src/{_THEME}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    def setLanguage(language, root: maliang.Tk):
        global FONT_FAMILY, FONT_FAMILY_BOLD
        log(f'Change locale to {language}.')

        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))

        if language == 'jp':
            FONT_FAMILY = 'Yu Gothic UI'
            FONT_FAMILY_BOLD = f'Yu Gothic UI Bold'
            FONT_FAMILY_LIGHT = f'Yu Gothic UI Light'
        elif language in ('cn', 'sb'):
            FONT_FAMILY = 'Microsoft YaHei UI'
            FONT_FAMILY_BOLD = f'Microsoft YaHei UI Bold'
            FONT_FAMILY_LIGHT = f'Microsoft YaHei UI Light'
        else:
            FONT_FAMILY = 'Segoe UI'
            FONT_FAMILY_BOLD = f'Segoe UI Semibold'  
            FONT_FAMILY_LIGHT = f'Segoe UI Light'

        global locale
        locale = language

        HEIGHT = 150
        lang_changebutton = []
        for i in lang_dict:
            lang_changebutton.append(
                maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55), command=lambda lang=i: setLanguage(lang, root),
                                image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD,
                                fontsize=18))
            HEIGHT += 60

        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))

        tmp = []
        for i in lang_dict:
            tmp.append(f'setlang_{i}')
        for i in range(len(lang_changebutton)):
            lang_changebutton[i].set(translate(tmp[i]))
        
        
        root.title(f'{translate("prodname")} {translate(_VERSION)}-{_SUBVERSION}')

    setLanguage(locale, root)

    root.mainloop()


def tracebackWindow(exception: Exception):
    log('Starting Traceback window because a exception detected.', type=WARN)
    root = maliang.Tk(size=(1500, 800), title=f'ArkLauncher {_VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=1500, height=800)

    text_title = maliang.Text(cv, (50, 50), family='Microsoft YaHei UI Bold', fontsize=23)
    text_title.set('An error detected.')

    text_title = maliang.Text(cv, (50, 75), family='Microsoft YaHei UI', fontsize=17)
    text_title.set('You can take an screenshot in this window, and send it to the author.')

    text_trace = maliang.Text(cv, (50, 130), family='Consolas', fontsize=14)

    text_trace.set(str(''.join(traceback.format_exception(exception))))
    

    root.center()
    root.mainloop()

    
def main():
    global locale
    log(f'Starting ATNetwork ArkLaucher GUI, version {_VERSION}.')

    loadLocale()
    locale = 'en'

    mainPage(500, 200)

    # welcomePage()

