# 最强大的maliang。。
import maliang
import data
import base64
import keyboard
from PIL import Image, ImageTk
from io import BytesIO

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

# 定义语言词典。
lang_dict = {
    'en': {
        'welcome': 'Welcome to ArkLauncher',
        'desc': 'Easily access and manage your Minecraft games.',
        'license': 'I agree to using this project with the MIT License.',
        'collect': 'Send anonymous data to help ATCraft Network\nimprove ArkLauncher App.',
        'button': 'Start',
        'lang_chinese': '中文',
        'lang_english': 'English'
    },
    'cn': {
        'welcome': '欢迎使用 ArkLauncher',
        'desc': '轻松访问并管理您的 Minecraft 游戏库。',
        'license': '我同意贡献，使用此项目时遵守 MIT License。',
        'collect': '发送匿名使用信息来协助 ATCraft Network 提升\nArkLauncher App 的使用体验。',
        'button': '开始使用',
        'lang_chinese': '中文',
        'lang_english': 'English'
    },
    'egg': {  # 彩蛋语言
        'welcome': '坐和放宽™《解压文件》发射器®️',
        'desc': '像软的微型副驾驶一样对我的手艺进行发射。🤖',
        'license': '我对郊狼发射器在我身上榨精提供猫编程域名许可',
        'collect': '发送你的todesk配置文件和账号密码，但你并非并非\n（你需要来自dream大王的权限才能拒绝，L）',
        'button': '弹射起步',
        'lang_chinese': '掌瓦APP',
        'lang_english': 'English'
    }
}

# 初始化欢迎页面
def welcomePage():
    root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    icon = Image.open(BytesIO(base64.b64decode(data.icon)))
    root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(icon.resize((32, 32))))

    maliang.Image(cv, (50, 75), image=ImageTk.PhotoImage(icon.resize((150, 150))))
    text_welcome = maliang.Text(cv, (50, 250), text='', family='Microsoft YaHei UI Bold', weight='bold', fontsize=30)
    text_desc = maliang.Text(cv, (50, 300), text='', family='Microsoft YaHei UI bold', fontsize=17)
    text_license = maliang.Text(cv, (85, 605), text='', family='Microsoft YaHei UI Bold', weight='bold', fontsize=15)
    text_collect = maliang.Text(cv, (85, 643), text='', family='Microsoft YaHei UI Bold', weight='bold', fontsize=15)
    text_button_chinese = maliang.Text(cv, (210, 709), text="中文", fontsize=17, family='Microsoft YaHei UI Bold')
    maliang.Text(cv, (330, 709), text="English", fontsize=17, family='Microsoft YaHei UI Bold')
    button = maliang.Button(cv, (50, 700), size=(100, 40), text='', fontsize=16, family='Microsoft YaHei UI Bold')
    button.disable(True)

    # 同意协议逻辑
    def agreeLicense(enable):
        button.disable(not enable)

    # 切换语言函数
    def changeLanguage(lang_key):
        # 根据 lang_key 切换对应语言
        lang = lang_dict.get(lang_key, lang_dict['en'])

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

    # 设置复选框和单选框，设置默认值和事件绑定
    maliang.CheckBox(cv, (50, 600), command=agreeLicense, default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=checkEggLanguage, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    # 初始化时使用中文
    changeLanguage('cn')

    root.mainloop()

# 启动程序
welcomePage()
