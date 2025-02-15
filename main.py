import os
import maliang
import darkdetect
import keyboard
from PIL import Image, ImageFont

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800


FONT_FAMILY = 'Microsoft YaHei UI'

# 我看看能不能导入字体...
icon = Image.open('src/icon.ico')
icon_about = Image.open(f'src/{darkdetect.theme()}/about.png')
icon_settings = Image.open(f'src/{darkdetect.theme()}/settings.png')
icon_return = Image.open(f'src/{darkdetect.theme()}/return.png')
icon_maliang = Image.open(f'src/Contributors/maliang.png')
avatar_Stevesuk0 = Image.open(f'src/Contributors/Stevesuk0.jpg')
avatar_bzym2 = Image.open(f'src/Contributors/bzym2.png')
avatar_Xiaokang2022 = Image.open(f'src/Contributors/Xiaokang2022.jpg')
avatar_theOmegaLabs = Image.open(f'src/Contributors/the-OmegaLabs.png')

#我给语言文件拉出去了啊

# 定义语言词典。
lang_dict = {
    'en':     {
        'welcome': 'Welcome to ArkLauncher',
        'desc': 'Easily access and manage your Minecraft games.',
        'license': 'I agree to using this project with the MIT License.',
        'collect': 'Send anonymous data to help ATCraft Network\nimprove ArkLauncher App.',
        'button': 'Start',
        'lang_chinese': '中文',
        'lang_english': 'English',
        'homepage': 'Homepage',
        'about'        : 'About',
        'version'      : 'Version',
        'contributors' : 'Contributors',
        'dev_uiux'     : 'UI/UX',
        'dev_coredev'  : 'Core Developer',
        'specialthanks': 'Special thanks',
        'maliang_desc' : 'A lightweight UI framework based on\ntkinter with all UI drawn in Canvas!',
        'dev_maliang'  : 'Developer of \'maliang\'',
        'omegalab_desc': 'Developing a next-generation Linux\necosystem.'
    },
    'cn': {
        'welcome'      : '欢迎使用 ArkLauncher',
        'desc'         : '轻松访问并管理您的 Minecraft 游戏库。',
        'license'      : '我同意贡献，使用此项目时遵守 MIT License。',
        'collect'      : '发送匿名使用信息来协助 ATCraft Network 提升\nArkLauncher App 的使用体验。',
        'button'       : '开始使用',
        'lang_chinese' : '中文',
        'lang_english' : 'English',
        'homepage'     : '主页',
        'about'        : '关于',
        'version'      : '版本',
        'contributors' : '贡献者',
        'dev_uiux'     : '界面设计',
        'dev_coredev'  : '核心开发者',
        'specialthanks': '特别感谢',
        'maliang_desc' : '一个基于 Tkinter 画布的轻量 UI 框架。',
        'dev_maliang'  : 'maliang 的开发者',
        'omegalab_desc': '构建下一代 Linux 生态系统。'
    },
    'egg': {  # 彩蛋语言
        'welcome': '坐和放宽™《解压文件》发射器®️',
        'desc': '像软的微型副驾驶一样对我的手艺进行发射。🤖',
        'license': '我对郊狼发射器在我身上榨精提供猫编程域名许可',
        'collect': '发送你的todesk配置文件和账号密码，但你并非并非\n（你需要来自dream大王的权限才能拒绝，L）',
        'button': '弹射起步',
        'lang_chinese': '掌瓦APP',
        'lang_english': 'English',
        'homepage':'洛杉矶',
        'about': '讲述人',
        'version': '圈钱',
        'contributors': '公交车',
        'dev_uiux': '吴旭淳',
        'dev_coredev': '摆烂大王',
        'specialthanks': '暗杀名单',
        'maliang_desc': '把屎山tkinter干掉的牛逼东西',
        'dev_maliang': '又一次听坚强笨女人听哭了',
        'omegalab_desc': '构建下一代水影并skid欣欣内部圈钱（大粉丝有神器）'
    }
}


def createWindow(x = None, y = None):
    if x and y: root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'ArkLauncher {VERSION}')
    else: root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32))))
    return root, cv

def changeWindow(window, root: maliang.Tk):
    x, y = root.winfo_x(), root.winfo_y()
    root.__exit__()
    window(x, y)

def welcomePage():
    global locale
    root, cv = createWindow()

    maliang.Image(cv, (50, 75), image=maliang.PhotoImage(icon.resize((150, 150))))

    text_welcome = maliang.Text(cv, (50, 250), text='', family=f'{FONT_FAMILY} Bold', weight='bold', fontsize=30)
    text_desc    = maliang.Text(cv, (50, 300), text='', family=f'{FONT_FAMILY} Bold', fontsize=17)
    text_license = maliang.Text(cv, (85, 605), text='', family=f'{FONT_FAMILY} Bold', weight='bold',fontsize=15)
    text_collect = maliang.Text(cv, (85, 643), text='', family=f'{FONT_FAMILY} Bold', weight='bold', fontsize=15)
    text_button_chinese = maliang.Text(cv, (210, 709), text="中文", fontsize=17, family=f'{FONT_FAMILY} Bold')
    maliang.Text(cv, (330, 709), text="English", fontsize=17, family=f'{FONT_FAMILY} Bold')
    button = maliang.Button(cv, (50, 700), size=(100, 40), command=lambda: changeWindow(mainPage, root), text='', fontsize=16, family=f'{FONT_FAMILY} Bold')
    button.disable(True)

    # 同意协议逻辑
    def agreeLicense(enable):
        button.disable(not enable)

    # 切换语言函数
    def changeLanguage(lang_key):   
        global locale
        lang = lang_dict.get(lang_key, lang_dict['en'])
        locale = lang_key

        text_welcome.set(lang['welcome'])
        text_desc.set(lang['desc'])
        text_license.set(lang['license'])
        text_collect.set(lang['collect'])
        text_button_chinese.set(lang['lang_chinese'])
        button.set(lang['button'])

    # 切换到英文
    def changeToEnglish(_):
        changeLanguage('en')

    # 处理按下 shift 键时的彩蛋语言
    def checkEggLanguage(_):
        if keyboard.is_pressed('shift'):  # 如果按下 Shift 键，切换到彩蛋语言
            changeLanguage('egg')
        else:
            changeLanguage('cn')

    maliang.CheckBox(cv, (50, 600), command=agreeLicense, default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=checkEggLanguage, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    # 初始化时使用中文
    changeLanguage('cn')

    root.mainloop()


def aboutPage(x, y):
    root, cv = createWindow(x, y)

    def openProfile(name):
        os.system(f'start https://github.com/{name}')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55))))
    text_logo1 = maliang.Text(cv, (113, 50), text='', family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), text='', family=f'{FONT_FAMILY} Bold', fontsize=26)

    maliang.IconButton(cv, (115, 145), size=(75, 75), image=maliang.PhotoImage(icon.resize((73, 73))), command=lambda: openProfile('the-OmegaLabs/ArkLauncher'))
    maliang.Text(cv, (200, 145), text='ATCraft Network', family=FONT_FAMILY, fontsize=18)
    maliang.Text(cv, (198, 165), text='ArkLauncher', family=f'{FONT_FAMILY} Bold', fontsize=30)
    text_version = maliang.Text(cv, (200, 205), text='', family=FONT_FAMILY, fontsize=15)

    text_contributor = maliang.Text(cv, (50, 250), text='', family=f'{FONT_FAMILY} Bold', fontsize=26)
    
    maliang.IconButton(cv, position=(50, 300), size=(50, 50), command=lambda: openProfile('Stevesuk0'), image=maliang.PhotoImage(avatar_Stevesuk0.resize((47, 47))))
    maliang.Text(cv, (115, 300), text='Stevesuk', family=f'{FONT_FAMILY} Bold', fontsize=25)
    text_Stevesuk0_desc = maliang.Text(cv, (115, 332), text='', family=FONT_FAMILY, fontsize=15)    

    maliang.IconButton(cv, position=(50, 360), size=(50, 50), command=lambda: openProfile('bzym2'), image=maliang.PhotoImage(avatar_bzym2.resize((47, 47))))
    maliang.Text(cv, (115, 360), text='BIZONUSERYAKAMO', family=f'{FONT_FAMILY} Bold', fontsize=25)
    text_bzym_desc = maliang.Text(cv, (115, 392), text='', family=FONT_FAMILY, fontsize=15)    

    text_thanks = maliang.Text(cv, (50, 450), text='', family=f'{FONT_FAMILY} Bold', fontsize=26)
    
    maliang.IconButton(cv, position=(50, 500), size=(50, 50), command=lambda: openProfile('Xiaokang2022/maliang'), image=maliang.PhotoImage(icon_maliang.resize((47, 47))))
    maliang.Text(cv, (115, 500), text='maliang', family=f'{FONT_FAMILY} Bold', fontsize=25)
    text_maliang_desc = maliang.Text(cv, (115, 532), text='', family=FONT_FAMILY, fontsize=15)    

    maliang.IconButton(cv, position=(50, 580), size=(50, 50), command=lambda: openProfile('Xiaokang2022'), image=maliang.PhotoImage(avatar_Xiaokang2022.resize((47, 47))))
    maliang.Text(cv, (115, 580), text='Zhikang Yan', family=f'{FONT_FAMILY} Bold', fontsize=25)
    text_Xiaokang2022_desc = maliang.Text(cv, (115, 612), text='', family=FONT_FAMILY, fontsize=15)    

    maliang.IconButton(cv, position=(50, 640), size=(50, 50), command=lambda: openProfile('the-OmegaLabs'), image=maliang.PhotoImage(avatar_theOmegaLabs.resize((47, 47))))
    maliang.Text(cv, (115, 640), text='Omega Labs', family=f'{FONT_FAMILY} Bold', fontsize=25)
    text_omegalab_desc = maliang.Text(cv, (115, 672), text='', family=FONT_FAMILY, fontsize=15)    

    lang = lang_dict.get(locale)

    text_logo1.set(lang['homepage'])
    text_logo2.set(lang['about'])
    text_version.set(f"{lang['version']}: {VERSION}")
    text_contributor.set(lang['contributors'])
    text_Stevesuk0_desc.set(f"{lang['dev_uiux']}, {lang['dev_coredev']}")
    text_bzym_desc.set(f"{lang['dev_uiux']}, {lang['dev_coredev']}")
    text_thanks.set(lang['specialthanks'])
    text_maliang_desc.set(lang['maliang_desc'])
    text_Xiaokang2022_desc.set(lang['dev_maliang'])
    text_omegalab_desc.set(lang['omegalab_desc'])
    root.mainloop()

def mainPage(x, y):
    root, cv = createWindow(x, y)
    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(aboutPage, root), image=maliang.PhotoImage(icon_about.resize((55, 55))))
    maliang.IconButton(cv, position=(340, 50), size=(50, 50), image=maliang.PhotoImage(icon_settings.resize((55, 55))))

    logo = maliang.Image(cv, (50, 50), image=maliang.PhotoImage(icon.resize((50, 50))))
    text_logo1 = maliang.Text(cv, (113, 50), text='ATCraft Network', family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 68), text='ArkLauncher', family=f'{FONT_FAMILY} Bold', fontsize=26)


    root.mainloop()

locale = 'cn'
welcomePage()

