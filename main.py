import json
import os
import platform
import colorama
import darkdetect
import keyboard
import maliang
import traceback
from PIL import Image

if platform.system() == 'Windows':
    import libs.winavatar as avatar
elif platform.system() == 'Linux':
    import libs.linavatar as avatar

from libs.olog import output as log
from libs.olog import WARN, ERROR, INFO, DEBUG

colorama.init()

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

FONT_FAMILY = 'Microsoft YaHei UI'
FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'


def openGithub(name):
    os.system(f'start https://github.com/{name}')


def createWindow(x=None, y=None):
    log(f'Creating new page at ({x}, {y}).')
    icon = Image.open('src/icon.png')
    if x and y:
        root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'ArkLauncher {VERSION}')
    else:
        root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32), 1)))
    return root, cv


def changeWindow(window, root: maliang.Tk):
    log(f'Perform change window to "{window.__name__}"...')
    x, y = root.winfo_x(), root.winfo_y()
    root.__exit__()
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
        if keyboard.is_pressed('shift'):  # 如果按下 Shift 键，切换到彩蛋语言
            changeLanguage('egg')
        else:
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
    root, cv = createWindow(x, y)

    icon = Image.open('src/icon.png')
    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')
    icon_maliang = Image.open(f'src/Contributors/maliang.png')
    avatar_Stevesuk0 = Image.open(f'src/Contributors/Stevesuk0.jpg')
    avatar_bzym2 = Image.open(f'src/Contributors/bzym2.png')
    avatar_suohoudaishi = Image.open(f'src/Contributors/SuoHouDaiShi.jpg')
    avatar_grassblock2022 = Image.open(f'src/Contributors/GrassBlock2022.png')
    avatar_Xiaokang2022 = Image.open(f'src/Contributors/Xiaokang2022.jpg')
    avatar_theOmegaLabs = Image.open(f'src/Contributors/the-OmegaLabs.png')

    maliang.Tooltip(
        maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1))), text=translate('return'))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, (110, 145), size=(75, 75), image=maliang.PhotoImage(icon.resize((73, 73))),
                       command=lambda: openGithub('the-OmegaLabs/ArkLauncher'))
    maliang.Text(cv, (202, 145), text=translate("parent"), family=FONT_FAMILY, fontsize=18)
    maliang.Text(cv, (200, 165), text=translate("prodname"), family=FONT_FAMILY_BOLD, fontsize=30)
    text_version = maliang.Text(cv, (200, 205), family=FONT_FAMILY, fontsize=15)

    text_contributor = maliang.Text(cv, (50, 250), family=FONT_FAMILY_BOLD, fontsize=26)
    maliang.IconButton(cv, position=(50, 300), size=(50, 50), command=lambda: openGithub('Stevesuk0'),
                       image=maliang.PhotoImage(avatar_Stevesuk0.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(110, 300), size=(50, 50), command=lambda: openGithub('bzym2'),
                       image=maliang.PhotoImage(avatar_bzym2.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(170, 300), size=(50, 50), command=lambda: openGithub('GrassBlock2022'),
                       image=maliang.PhotoImage(avatar_grassblock2022.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(230, 300), size=(50, 50), command=lambda: openGithub('SuoHouDaiShi'),
                       image=maliang.PhotoImage(avatar_suohoudaishi.resize((47, 47), 1)))

    text_thanks = maliang.Text(cv, (50, 450), family=FONT_FAMILY_BOLD, fontsize=26)
    maliang.IconButton(cv, position=(50, 500), size=(50, 50), command=lambda: openGithub('Xiaokang2022/maliang'),
                       image=maliang.PhotoImage(icon_maliang.resize((35, 35), 1)))
    maliang.Text(cv, (115, 500), text='maliang', family=FONT_FAMILY_BOLD, fontsize=25)
    text_maliang_desc = maliang.Text(cv, (115, 532), family=FONT_FAMILY, fontsize=15)
    maliang.IconButton(cv, position=(50, 570), size=(50, 50), command=lambda: openGithub('Xiaokang2022'),
                       image=maliang.PhotoImage(avatar_Xiaokang2022.resize((47, 47), 1)))
    maliang.Text(cv, (115, 570), text='Zhikang Yan', family=FONT_FAMILY_BOLD, fontsize=25)
    text_Xiaokang2022_desc = maliang.Text(cv, (115, 602), family=FONT_FAMILY, fontsize=15)
    maliang.IconButton(cv, position=(50, 640), size=(50, 50), command=lambda: openGithub('the-OmegaLabs'),
                       image=maliang.PhotoImage(avatar_theOmegaLabs.resize((47, 47), 1)))
    maliang.Text(cv, (115, 640), text='Omega Labs', family=FONT_FAMILY_BOLD, fontsize=25)
    text_omegalab_desc = maliang.Text(cv, (115, 672), family=FONT_FAMILY, fontsize=15)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('about'))
    text_version.set(f"{translate('version')}: {VERSION}")
    text_contributor.set(translate('contributors'))
    text_thanks.set(translate('specialthanks'))
    text_maliang_desc.set(translate('maliang_desc'))
    text_Xiaokang2022_desc.set(translate('dev_maliang'))
    text_omegalab_desc.set(translate('omegalab_desc'))
    root.mainloop()


def mainPage(x, y):
    root, cv = createWindow(x, y)

    icon = Image.open('src/icon.png')
    icon_about = Image.open(f'src/{darkdetect.theme()}/about.png')
    icon_settings = Image.open(f'src/{darkdetect.theme()}/settings.png')
    icon_quick = Image.open(f'src/{darkdetect.theme()}/quick.png')
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

    root.mainloop()


def settingsPage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')
    icon_about = Image.open(f'src/{darkdetect.theme()}/about.png')
    icon_language = Image.open(f'src/{darkdetect.theme()}/language.png')
    icon_network = Image.open(f'src/{darkdetect.theme()}/network.png')
    icon_avatar = Image.open(avatar.getAvatar())
    icon_account = Image.open(f'src/{darkdetect.theme()}/account.png')
    icon_customize = Image.open(f'src/{darkdetect.theme()}/customize.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
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
    button_account.set(f' {translate('account')}')
    button_language.set(f' {translate('locale')}')
    button_network.set(f' {translate('network')}')
    button_about.set(f' {translate('about')}')
    button_customize.set(f' {translate('customize')}')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    root.mainloop()


def settingsAccountPage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('account'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    root.mainloop()


def settingsNetworkPage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('network'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    root.mainloop()


def settingsCustomizePage(x, y):
    root, cv = createWindow(x, y)

    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('customize'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

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
    global locale
    root, cv = createWindow(x, y)

    icon_language = Image.open(f'src/{darkdetect.theme()}/language.png')
    icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')

    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    HEIGHT = 150
    lang_changebutton = []
    for i in lang_dict:
        lang_changebutton.append(
            maliang.IconButton(cv, position=(50, HEIGHT), size=(400, 55), command=lambda lang=i: setLanguage(lang),
                               image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD,
                               fontsize=18))
        HEIGHT += 60

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('locale'))

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root),
                           image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))

    def setLanguage(language):
        log(f'Change locale to {language}.')
        global locale
        locale = language
        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))
        tmp = []
        for i in lang_dict:
            tmp.append(f'setlang_{i}')
        for i in range(len(lang_changebutton)):
            lang_changebutton[i].set(translate(tmp[i]))

    setLanguage(locale)

    root.mainloop()


def main():
    global locale
    log(f'Starting ATCraft ArkLaucher, version {VERSION}.')

    loadLocale()
    locale = 'en'

    mainPage(500, 200)

    # welcomePage()

def tracebackWindow(exception: Exception):
    log('Starting Traceback window because a exception detected.', type=WARN)
    icon = Image.open('src/icon.png')
    root = maliang.Tk(size=(1000, 500), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=1000, height=500)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32), 1)))

    text_title = maliang.Text(cv, (50, 50), family=FONT_FAMILY_BOLD, fontsize=23)
    text_title.set('An error detected.')

    text_title = maliang.Text(cv, (50, 85), family=FONT_FAMILY, fontsize=17)
    text_title.set('You can take an screenshot in this window, and send it to the author.')

    text_trace = maliang.Text(cv, (50, 150), family='Consolas', fontsize=14)

    text_trace.set(str('\n'.join(traceback.format_exception(exception))))
    

    root.center()
    root.mainloop()

    

try:
    main()
except Exception as f:
    log(f, type=ERROR)
    tracebackWindow(f)