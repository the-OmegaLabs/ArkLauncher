import os
import maliang
import darkdetect
import keyboard
import libs.winavatar
from PIL import Image, ImageFont    

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

FONT_FAMILY = 'Microsoft YaHei UI'
FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'

lang_dict = {
    'en':     {
        'welcome': 'Welcome to ArkLauncher',
        'desc': 'Easily access and manage your Minecraft games.',
        'license': 'I agree to using this project with the MIT License.',
        'collect': 'Send anonymous data to help ATCraft Network\nimprove ArkLauncher App.',
        'button': 'Start',
        'language': 'Language',
        'lang_chinese': '中文',
        'lang_english': 'English',
        'homepage': 'Homepage',
        'account': 'ATCraft ID',
        'about': 'About',
        'settings': 'Settings',
        'network': 'Networking',
        'version': 'Version',
        'locale': 'Language & Region',
        'contributors': 'Contributors',
        'dev_uiux': 'UI/UX',
        'dev_coredev': 'Core Developer',
        'specialthanks': 'Special thanks',
        'maliang_desc': 'A lightweight UI framework for python.',
        'dev_maliang': 'Developer of \'maliang\'',
        'setlang_cn': '中文 (Chinese)',
        'setlang_en': 'English',
        'setlang_jp': '日本語 (Japanese)',
        'setlang_sb': '精通八国语言 (Chinese with meme)',
        'omegalab_desc': 'Developing a next-generation Linux\necosystem.',
        'missing': '{Missing}',
    },
    'cn': {
        'welcome': '欢迎使用 ArkLauncher',
        'desc': '轻松访问并管理您的 Minecraft 游戏库。',
        'license': '我同意贡献，使用此项目时遵守 MIT License。',
        'collect': '发送匿名使用信息来协助 ATCraft Network 提升\nArkLauncher App 的使用体验。',
        'button': '开始使用',
        'language': '语言',
        'lang_chinese': '中文',
        'lang_english': 'English',
        'homepage': '主页',
        'about': '关于',
        'account': 'ATCraft ID',
        'settings': '设置',
        'version': '版本',
        'locale': '语言与地区',
        'network': '网络',
        'contributors': '贡献者',
        'dev_uiux': '界面设计',
        'dev_coredev': '核心开发者',
        'specialthanks': '特别感谢',
        'maliang_desc': '一个使用 Python 编写的轻量 UI 框架。',
        'dev_maliang': 'maliang 的开发者',
        'setlang_cn': '中文',
        'setlang_en': 'English (英语)',
        'setlang_sb': '精通八国语言 (梗体中文)',
        'setlang_jp': '日本語 (日语)',
        'omegalab_desc': '构建下一代 Linux 生态系统。',
        'missing': '{缺少翻译}',
    },
    'jp': {
        'welcome': 'ArkLauncherをご利用いただきありがとうございます',
        'desc': 'Minecraftゲームライブラリを簡単にアクセスし、管理できます。',
        'license': '貢献に同意し、このプロジェクトの使用に際してMITライセンスに従います。',
        'collect': 'ATCraft NetworkがArkLauncherアプリの使用体験を向上させるための匿名使用情報を送信します。',
        'button': '使用を開始する',
        'language': '言語',
        'lang_chinese': '中国語',
        'lang_english': '英語',
        'homepage': 'ホームページ',
        'about': 'このアプリについて',
        'settings': '設定',
        'version': 'バージョン',
        'locale': '言語と地域',
        'contributors': '貢献者',
        'dev_uiux': 'UIデザイン',
        'dev_coredev': 'コア開発者',
        'specialthanks': '特別な感謝',
        'maliang_desc': 'Pythonで書かれた軽量UIフレームワーク。',
        'dev_maliang': 'maliangの開発者',
        'setlang_cn': '中文 (中国語)',
        'setlang_en': 'English (英語)',
        'setlang_sb': '精通八国语言 (梗体中国語)',
        'setlang_jp': '日本語',
        'omegalab_desc': '次世代Linuxエコシステムの構築。',
        'missing': '{翻訳がありません}',
    },
    'egg': {  # 彩蛋语言
        'welcome': '坐和放宽™《解压文件》发射器®️',
        'desc': '像软的微型副驾驶一样对我的手艺进行发射。🤖',
        'license': '我对郊狼发射器在我身上榨精提供猫编程域名许可',
        'collect': '发送你的 todesk 配置文件和账号密码，但你并非并非\n（你需要来自dream大王的权限才能拒绝，L）',
        'button': '弹射起步',
        'lang_chinese': '掌瓦APP',
        'lang_english': '崇洋媚外',
        'homepage': '洛杉矶',
        'about': '讲述人',
        'settings': '仪表',
        'account': '录管系统',
        'locale': '你永远是中国人',
        'network': '天翼3G',
        'version': '圈钱',
        'missing': '{缺少傻逼在这里拉屎}',
        'contributors': '公交车',
        'dev_uiux': '吴旭淳',
        'dev_coredev': '摆烂大王',
        'specialthanks': '暗杀名单',
        'maliang_desc': '把屎山 tkinter 干掉的牛逼东西',
        'dev_maliang': '你们都不许骂他他是我爹',
        'setlang_cn': '华为手机 (增智慧)',
        'setlang_en': 'iPhone (自适应)',
        'setlang_sb': '公共厕所',
        'setlang_jp': 'かおにまで (孙笑川国)',
        'omegalab_desc': '构建下一代水影并 skid 欣欣内部圈钱（大粉丝有神器）'
    },
    'star': {
        'welcome': '**** ***********',
        'desc': '********* ********* ***',
        'license': '***** ** ****** *** *******',
        'collect': '*********** ******* ******* **\n*********** *** *****',
        'button': '****',
        'language': '**',
        'lang_chinese': '**',
        'lang_english': '*******',
        'homepage': '**',
        'about': '**',
        'account': '******* **',
        'settings': '**',
        'version': '**',
        'locale': '*****',
        'network': '**',
        'contributors': '***',
        'dev_uiux': '****',
        'dev_coredev': '*****',
        'specialthanks': '****',
        'maliang_desc': '**** ****** ***** ** **',
        'dev_maliang': '******* ****',
        'setlang_cn': '**',
        'setlang_en': '******* (**)',
        'setlang_sb': '****** (****)',
        'setlang_jp': '*** (**)',
        'omegalab_desc': '***** ***** ****',
        'missing': '{:****:}',
    }
}

def openGithub(name):
    os.system(f'start https://github.com/{name}')

def translate(target):
    return lang_dict[locale].get(target, lang_dict[locale]['missing'])


def createWindow(x = None, y = None):
    icon = Image.open('src/icon.png')
    if x and y: root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'ArkLauncher {VERSION}')
    else: root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32), 1)))
    return root, cv

def changeWindow(window, root: maliang.Tk):
    x, y = root.winfo_x(), root.winfo_y()
    root.__exit__()
    window(x, y)

def welcomePage():
    global locale
    root, cv = createWindow()
    
    icon = Image.open('src/icon.png')
    
    maliang.Image(cv, (50, 75), image=maliang.PhotoImage(icon.resize((150, 150), 1)))
    text_welcome = maliang.Text(cv, (50, 250), family=FONT_FAMILY_BOLD, fontsize=30)
    text_desc    = maliang.Text(cv, (50, 300), family=FONT_FAMILY_BOLD, fontsize=17)
    text_license = maliang.Text(cv, (85, 605), family=FONT_FAMILY_BOLD, fontsize=15)
    text_collect = maliang.Text(cv, (85, 643), family=FONT_FAMILY_BOLD, fontsize=15)
    text_button_chinese = maliang.Text(cv, (210, 709), text="中文", fontsize=17, family=FONT_FAMILY_BOLD)
    maliang.Text(cv, (330, 709), text="English", fontsize=17, family=FONT_FAMILY_BOLD)
    button = maliang.Button(cv, (50, 700), size=(100, 40), command=lambda: changeWindow(mainPage, root), fontsize=16, family=FONT_FAMILY_BOLD)
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
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish , length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    # 初始化时使用中文
    changeLanguage('cn')

    root.mainloop()

def aboutPage(x, y):
    root, cv = createWindow(x, y)

    icon                  = Image.open('src/icon.png')       
    icon_return           = Image.open(f'src/{darkdetect.theme()}/return.png')
    icon_maliang          = Image.open(f'src/Contributors/maliang.png')
    avatar_Stevesuk0      = Image.open(f'src/Contributors/Stevesuk0.jpg')
    avatar_bzym2          = Image.open(f'src/Contributors/bzym2.png')
    avatar_suohoudaishi   = Image.open(f'src/Contributors/SuoHouDaiShi.jpg')
    avatar_grassblock2022 = Image.open(f'src/Contributors/GrassBlock2022.png')
    avatar_Xiaokang2022   = Image.open(f'src/Contributors/Xiaokang2022.jpg')
    avatar_theOmegaLabs   = Image.open(f'src/Contributors/the-OmegaLabs.png')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, (110, 145), size=(75, 75), image=maliang.PhotoImage(icon.resize((73, 73))), command=lambda: openGithub('the-OmegaLabs/ArkLauncher'))
    maliang.Text(cv, (202, 145), text='ATCraft Network', family=FONT_FAMILY, fontsize=18)
    maliang.Text(cv, (200, 165), text='ArkLauncher', family=FONT_FAMILY_BOLD, fontsize=30)
    text_version = maliang.Text(cv, (200, 205), family=FONT_FAMILY, fontsize=15)

    text_contributor = maliang.Text(cv, (50, 250), family=FONT_FAMILY_BOLD, fontsize=26)    
    maliang.IconButton(cv, position=(50, 300), size=(50, 50), command=lambda: openGithub('Stevesuk0'), image=maliang.PhotoImage(avatar_Stevesuk0.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(110, 300), size=(50, 50), command=lambda: openGithub('bzym2'), image=maliang.PhotoImage(avatar_bzym2.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(170, 300), size=(50, 50), command=lambda: openGithub('GrassBlock2022'), image=maliang.PhotoImage(avatar_grassblock2022.resize((47, 47), 1)))
    maliang.IconButton(cv, position=(230, 300), size=(50, 50), command=lambda: openGithub('SuoHouDaiShi'), image=maliang.PhotoImage(avatar_suohoudaishi.resize((47, 47), 1)))

    text_thanks = maliang.Text(cv, (50, 450), family=FONT_FAMILY_BOLD, fontsize=26)
    maliang.IconButton(cv, position=(50, 500), size=(50, 50), command=lambda: openGithub('Xiaokang2022/maliang'), image=maliang.PhotoImage(icon_maliang.resize((35, 35), 1)))
    maliang.Text(cv, (115, 500), text='maliang', family=FONT_FAMILY_BOLD, fontsize=25)
    text_maliang_desc = maliang.Text(cv, (115, 532), family=FONT_FAMILY, fontsize=15)
    maliang.IconButton(cv, position=(50, 570), size=(50, 50), command=lambda: openGithub('Xiaokang2022'), image=maliang.PhotoImage(avatar_Xiaokang2022.resize((47, 47), 1)))
    maliang.Text(cv, (115, 570), text='Zhikang Yan', family=FONT_FAMILY_BOLD, fontsize=25)
    text_Xiaokang2022_desc = maliang.Text(cv, (115, 602), family=FONT_FAMILY, fontsize=15)
    maliang.IconButton(cv, position=(50, 640), size=(50, 50), command=lambda: openGithub('the-OmegaLabs'), image=maliang.PhotoImage(avatar_theOmegaLabs.resize((47, 47), 1)))
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
    
    icon          = Image.open('src/icon.png')   
    icon_about    = Image.open(f'src/{darkdetect.theme()}/about.png')
    icon_settings = Image.open(f'src/{darkdetect.theme()}/settings.png')
    icon_quick    = Image.open(f'src/{darkdetect.theme()}/quick.png')
    icon_testGame = Image.open(f'src/project/candee.png')

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_settings.resize((55, 55), 1)))
    maliang.IconButton(cv, position=(340, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root), image=maliang.PhotoImage(icon_quick.resize((40, 40), 1)))


    maliang.Image(cv, (50, 50), image=maliang.PhotoImage(icon.resize((50, 50), 1)))
    maliang.Text(cv, (110, 50), text='ATCraft Network', family=FONT_FAMILY, fontsize=15)
    maliang.Text(cv, (110, 68), text='ArkLauncher', family=FONT_FAMILY_BOLD, fontsize=26)

    icon_cs2 = Image.open(f'src/project/cs2_icon.jpg')
    button_cs2 = maliang.Button(cv, position=(50, 130), size=(400, 100))
    maliang.Image(button_cs2, position=(25, 25), image=maliang.PhotoImage(icon_cs2.resize((50, 50), 1)))
    maliang.Text(button_cs2, (100, 20), text='Counter-Strike 2', family=FONT_FAMILY_BOLD, fontsize=26)
    maliang.Text(button_cs2, (100, 60), text='A 5v5 firstperson tactical shooter.', family=FONT_FAMILY, fontsize=15)

    
    button_new = maliang.Button(cv, position=(50, 250), size=(400, 100))
    maliang.Text(button_new, (200, 50), text='+', family=FONT_FAMILY_BOLD, fontsize=50, anchor='center')
    

    

    root.mainloop()

def settingsPage(x, y):
    root, cv = createWindow(x, y)

    icon_return    = Image.open(f'src/{darkdetect.theme()}/return.png')
    icon_about     = Image.open(f'src/{darkdetect.theme()}/about.png')
    icon_language  = Image.open(f'src/{darkdetect.theme()}/language.png')
    icon_network  = Image.open(f'src/{darkdetect.theme()}/network.png')
    icon_avatar    = Image.open(libs.winavatar.getAvatar())
    icon_account   = Image.open(f'src/{darkdetect.theme()}/account.png')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(mainPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_avatar.resize((45, 45), 1)))

    button_account  = maliang.IconButton(cv, position=(50, 150), size=(400, 55), command=lambda: changeWindow(settingsAccountPage, root), image=maliang.PhotoImage(icon_account.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_language = maliang.IconButton(cv, position=(50, 210), size=(400, 55), command=lambda: changeWindow(settingsLanguagePage, root), image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_network  = maliang.IconButton(cv, position=(50, 270), size=(400, 55), command=lambda: changeWindow(settingsNetworkPage, root), image=maliang.PhotoImage(icon_network.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_about    = maliang.IconButton(cv, position=(50, 330), size=(400, 55), command=lambda: changeWindow(aboutPage, root), image=maliang.PhotoImage(icon_about.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)

    text_logo1.set(translate('homepage'))
    text_logo2.set(translate('settings'))
    button_account.set(f' {translate('account')}')
    button_language.set(f' {translate('locale')}')
    button_network.set(f' {translate('network')}')
    button_about.set(f' {translate('about')}')

    root.mainloop()

def settingsAccountPage(x, y):
    root, cv = createWindow(x, y)

    icon_return     = Image.open(f'src/{darkdetect.theme()}/return.png')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('account')) 

    root.mainloop()

def settingsNetworkPage(x, y):
    root, cv = createWindow(x, y)

    icon_return     = Image.open(f'src/{darkdetect.theme()}/return.png')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    text_logo1.set(translate('settings'))
    text_logo2.set(translate('network')) 

    root.mainloop()

def settingsLanguagePage(x, y):
    global locale
    root, cv = createWindow(x, y)

    icon_language   = Image.open(f'src/{darkdetect.theme()}/language.png')
    icon_return     = Image.open(f'src/{darkdetect.theme()}/return.png')

    maliang.IconButton(cv, position=(50, 50), size=(50, 50), command=lambda: changeWindow(settingsPage, root), image=maliang.PhotoImage(icon_return.resize((55, 55), 1)))
    text_logo1 = maliang.Text(cv, (110, 50), family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 70), family=FONT_FAMILY_BOLD, fontsize=26)

    button_changeToCN = maliang.IconButton(cv, position=(50, 150), size=(400, 55), command=lambda: setLanguage('cn'), image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_changeToEN = maliang.IconButton(cv, position=(50, 210), size=(400, 55), command=lambda: setLanguage('en'), image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_changeToSB = maliang.IconButton(cv, position=(50, 270), size=(400, 55), command=lambda: setLanguage('egg'), image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)
    button_changeToJP = maliang.IconButton(cv, position=(50, 330), size=(400, 55), command=lambda: setLanguage('jp'), image=maliang.PhotoImage(icon_language.resize((40, 40), 1)), family=FONT_FAMILY_BOLD, fontsize=18)


    text_logo1.set(translate('settings'))
    text_logo2.set(translate('locale')) 
    button_changeToCN.set(translate('setlang_cn'))
    button_changeToEN.set(translate('setlang_en'))
    button_changeToSB.set(translate('setlang_sb'))
    button_changeToJP.set(translate('setlang_jp'))

    def setLanguage(language):
        global locale
        locale = language    
        text_logo1.set(translate('settings'))
        text_logo2.set(translate('locale'))
        button_changeToCN.set(translate('setlang_cn'))
        button_changeToEN.set(translate('setlang_en'))
        button_changeToSB.set(translate('setlang_sb'))
        button_changeToJP.set(translate('setlang_jp'))
    root.mainloop()


locale = 'en'
mainPage(500, 200)
#welcomePage()

