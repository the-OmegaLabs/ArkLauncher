import maliang
from PIL import Image
import maliang.theme

WINDOW_SIZE = (1200, 700)

root = maliang.Tk(size=WINDOW_SIZE, title='ArkLauncher | 林泽钦小朋友该写作业了。')
root.icon(maliang.PhotoImage(Image.open('Resources/updater/icon.png')))
root.maxsize(WINDOW_SIZE[0], WINDOW_SIZE[1])
root.minsize(WINDOW_SIZE[0], WINDOW_SIZE[1])
maliang.theme.manager.customize_window(root, disable_maximize_button=True)


cv = maliang.Canvas(root)

cv.place(width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

nihui = maliang.Image(cv, position=(0, 0), image=maliang.PhotoImage(Image.open('Resources/updater/main.png')))


maliang.Text(cv, position=(15, 15), text='Checking update...', fontsize=20, family='Microsoft YaHei UI Bold')

root.mainloop()