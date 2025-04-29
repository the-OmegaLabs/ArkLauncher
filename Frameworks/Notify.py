import maliang
import maliang.animation
import threading
from Frameworks.Utils import play

ANIMATION_DURATION = 300
ANIMATION_FPS = 1000
SCALE = 1
FONT_FAMILY      = f'Microsoft YaHei UI'
FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
WIDTH = 350
HEIGHT = 100

def scaled(n): return n * SCALE

def toast(title, message, duration, icon, root, target = 'notify'):
    play(target)
    toast = maliang.Toplevel(root, size=(scaled(WIDTH), scaled(HEIGHT)), position=(10000, 10000), focus=False)
    toast.alpha(0.85)
    toast.geometry(position=(toast.winfo_screenwidth() // 2 - scaled(WIDTH) // 2, 0 - scaled(HEIGHT)))
    toast.overrideredirect(True)
    cv = maliang.Canvas(toast)
    cv.place(x = 0, y = 0, width = scaled(WIDTH), height=scaled(HEIGHT))

    maliang.animation.MoveWindow(
        window = toast, offset = (0, scaled(HEIGHT)), 
        duration = ANIMATION_DURATION, 
        controller = maliang.animation.ease_out, fps = ANIMATION_FPS
    ).start()
    
    maliang.animation.MoveWindow(
        window = toast, offset = (0, 0 - scaled(HEIGHT)), 
        duration = int(ANIMATION_DURATION * 1.5), fps = ANIMATION_FPS, 
        #end = lambda: (cv.after(1000, toast.destroy))
    ).start(delay=duration - ANIMATION_DURATION - 200)
    
    maliang.Image(
        master = cv, position = (scaled(HEIGHT) // 2, scaled(HEIGHT) // 2),
        image = maliang.PhotoImage(icon), anchor = 'center'
    )
    
    maliang.Text(
        master = cv, position = (scaled(HEIGHT // 1.1), scaled(HEIGHT // 3.5)),
        text = title, family = FONT_FAMILY_BOLD, fontsize=18
    )

    maliang.Text(
        master = cv, position = (scaled(HEIGHT // 1.1), scaled(HEIGHT // 1.75)),
        text=message, family=FONT_FAMILY, fontsize=16

    )

