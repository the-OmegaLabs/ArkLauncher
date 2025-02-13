import maliang
import data
import base64
import maliang.animation as animation
from PIL import Image, ImageTk
from io import BytesIO

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

def welcomePage():
    root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    icon = Image.open(BytesIO(base64.b64decode(data.icon)))
    root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(icon.resize((32, 32))))

    maliang.Image(cv, (50, 75), image=ImageTk.PhotoImage(icon.resize((150, 150))))
    maliang.Text(cv, (50, 250), text='欢迎使用 ArkLauncher', family='Microsoft YaHei UI Bold', weight='bold', fontsize=30)

    maliang.Text(cv, (50, 300), text='轻松管理并更新您的游戏。', family='Microsoft YaHei UI bold', fontsize=17)

    maliang.CheckBox(cv, (50, 600), command=print, default=False, length=23)
    maliang.Text(cv, (85, 605), text="我同意并遵守 MIT License。", family='Microsoft YaHei UI Bold', weight='bold',
                    fontsize=15)
    maliang.CheckBox(cv, (50, 640), command=print, default=True, length=23)
    maliang.Text(cv, (85, 643), text="发送匿名使用信息来协助 ATCraft Network 提升\nArkLauncher App 的使用体验。",
                    family='Microsoft YaHei UI Bold', weight='bold', fontsize=15)

    maliang.Button(cv, (50, 700), size=(100, 40), text='开始使用', fontsize=16, family='Microsoft YaHei UI Bold')

    maliang.RadioBox(cv, (170, 705), command=print, length=30, default=True)
    maliang.Text(cv, (210, 709), text="中文", fontsize=17, family='Microsoft YaHei UI Bold')

    maliang.RadioBox(cv, (260, 705), command=print, length=30, default=False)
    maliang.Text(cv, (300, 709), text="English", fontsize=17, family='Microsoft YaHei UI Bold')
    
    root.mainloop()

welcomePage()
