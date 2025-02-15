import maliang
import keyboard
import maliang.animation as animation
from PIL import Image, ImageTk

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

icon = Image.open('icon.ico')

def createWindow(x = None, y = None):
    if x and y: root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'ArkLauncher {VERSION}')
    else: root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(icon.resize((32, 32))))
    return root, cv

def changeWindow(window, root: maliang.Tk, x, y):
    root.__exit__()
    window(x, y)

def welcomePage():
    root, cv = createWindow()  

    maliang.Image(cv, (50, 75), image=ImageTk.PhotoImage(icon.resize((150, 150))))
    text_welcome = maliang.Text(cv, (50, 250), text='', family='Microsoft YaHei UI Bold', weight='bold', fontsize=30)
    text_desc    = maliang.Text(cv, (50, 300), text='', family='Microsoft YaHei UI bold', fontsize=17)
    text_license = maliang.Text(cv, (85, 605), text='', family='Microsoft YaHei UI Bold', weight='bold',fontsize=15)
    text_collect = maliang.Text(cv, (85, 643), text='', family='Microsoft YaHei UI Bold', weight='bold', fontsize=15)
    text_button_chinese = maliang.Text(cv, (210, 709), text="中文", fontsize=17, family='Microsoft YaHei UI Bold')
    maliang.Text(cv, (330, 709), text="English", fontsize=17, family='Microsoft YaHei UI Bold')
    button = maliang.Button(cv, (50, 700), size=(100, 40), text='', fontsize=16, family='Microsoft YaHei UI Bold')
    button.disable(True)

    def agreeLicense(enable):
        if enable:
            button.disable(False)
        else:
            button.disable(True)

    def changeToEnglish(_):
        text_welcome.set('Welcome to ArkLauncher')
        text_desc.set('Easily access and manage your Minecraft games.')
        text_license.set('I agree to using this project with the MIT License.')
        text_collect.set('Send anonymous data to help ATCraft Network\nimprove ArkLauncher App. (Decoration)')
        button.set('Start')

    def changeToChinese(_):
        if keyboard.is_pressed('shift'):
            text_welcome.set('坐和放宽™《解压文件》发射器®️')
            text_desc.set('像软的微型副驾驶一样对我的手艺进行发射。🤖')
            text_license.set('我对郊狼发射器在我身上榨精提供猫编程域名许可')
            text_collect.set('发送你的todesk配置文件和账号密码，但你并非并非\n（你需要来自dream大王的权限才能拒绝，L）')
            text_button_chinese.set('掌瓦APP')
            button.set('弹射起步')
        else:
            text_welcome.set('欢迎使用 ArkLauncher')
            text_desc.set('轻松访问并管理您的 Minecraft 游戏库。')
            text_license.set('我同意贡献，使用此项目时遵守 MIT License。')
            text_collect.set('发送匿名使用信息来协助 ATCraft Network 提升\nArkLauncher App 的使用体验。(摆设)')
            text_button_chinese.set('中文')
            button.set('开始使用')

    maliang.CheckBox(cv, (50, 600), command=agreeLicense, default=False, length=23)
    maliang.CheckBox(cv, (50, 640), default=True, length=23)
    langEN = maliang.RadioBox(cv, (290, 705), command=changeToEnglish, length=30, default=False)
    langCN = maliang.RadioBox(cv, (170, 705), command=changeToChinese, length=30, default=True)
    maliang.RadioBox.group(langCN, langEN)

    changeToChinese(1)

    root.mainloop()

def mainPage(x, y):
    root, cv = createWindow(x, y)
    logo = maliang.Image(cv, (50, 50), image=ImageTk.PhotoImage(icon.resize((50, 50))))
    text_logo1 = maliang.Text(cv, (113, 50), text='ATCraft Network', family='Microsoft YaHei UI', fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 68), text='ArkLauncher', family='Microsoft YaHei UI Bold', fontsize=26)
    

    root.mainloop()

welcomePage()