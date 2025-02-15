import maliang
import darkdetect
import keyboard
from PIL import Image

# 这个不影响你弄 我先试试
# ok

VERSION = 'Dev'
WIDTH = 500
HEIGHT = 800

def createWindow(x = None, y = None):
    if x and y: root = maliang.Tk(size=(WIDTH, HEIGHT), position=(x, y), title=f'ArkLauncher {VERSION}')
    else: root = maliang.Tk(size=(WIDTH, HEIGHT), title=f'ArkLauncher {VERSION}')
    root.resizable(0, 0)
    cv = maliang.Canvas(root)
    cv.place(width=WIDTH, height=HEIGHT)
    root.tk.call('wm', 'iconphoto', root._w, maliang.PhotoImage(icon.resize((32, 32))))
    return root, cv

def about_page(root, cv):
    root.mainloop()

def main_page(view):
    root, cv = createWindow() # cv = canvas 然后就自动绑定控价了？ 
    # 可以去翻翻教程： https://xiaokang2022.github.io/maliang-docs/3.0/tutorials/chapter_03/1/
    view.components['logo']=maliang.Image(cv, (50, 50), image=maliang.PhotoImage(icon.resize((50, 50))))



    logo = maliang.Image(cv, (50, 50), image=maliang.PhotoImage(icon.resize((50, 50))))
    text_logo1 = maliang.Text(cv, (113, 50), text='ATCraft Network', family=FONT_FAMILY, fontsize=15)
    text_logo2 = maliang.Text(cv, (110, 68), text='ArkLauncher', family=f'{FONT_FAMILY} Bold', fontsize=26)

    maliang.IconButton(cv, position=(400, 50), size=(50, 50), command=lambda: change_window(about_page, root), image=maliang.PhotoImage(icon_about.resize((55, 55))))
    maliang.IconButton(cv, position=(340, 50), size=(50, 50), image=maliang.PhotoImage(icon_settings.resize((55, 55))))

    root.mainloop()


class View:
    def __init__(self):
        pass

    components = {}
