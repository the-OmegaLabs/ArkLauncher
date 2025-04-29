import maliang
import maliang.animation

ANIMATION_DURATION = 700
ANIMATION_FPS = 1000
SCALE = 1
FONT_FAMILY      = f'Microsoft YaHei UI'
FONT_FAMILY_BOLD = f'{FONT_FAMILY} Bold'
WIDTH = 350
HEIGHT = 100

def scaled(n): return n * SCALE

def toast(title, message, duration, icon, root):
    toast = maliang.Toplevel(root, size=(scaled(WIDTH), scaled(HEIGHT)), position=(root.winfo_screenwidth(), scaled(50)), focus=False)
    toast.overrideredirect(True)
    cv = maliang.Canvas(toast)
    cv.place(x = 0, y = 0, width = scaled(WIDTH), height=scaled(HEIGHT))

    maliang.animation.MoveWindow(
        window = toast, offset = (0 - scaled(WIDTH), 0), 
        duration = ANIMATION_DURATION, 
        controller = maliang.animation.ease_out, fps = ANIMATION_FPS
    ).start()
    
    maliang.animation.MoveWindow(
        window = toast, 
        offset = (scaled(WIDTH), 0), 
        duration = ANIMATION_DURATION + 200, 
        controller = maliang.animation.ease_out, 
        fps = ANIMATION_FPS, 
        end = toast.destroy
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