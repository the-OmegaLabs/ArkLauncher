import maliang.toolbox
import socket
from PIL import Image, ImageDraw, ImageFilter, ImageGrab


def makeImageRadius(img, radius=30, alpha=0.5):
    img = img.convert("RGBA")

    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)

    draw.rounded_rectangle(
        (0, 0, img.size[0], img.size[1]), radius, fill=int(256 * alpha))

    img.putalpha(mask)

    return img

def takeShot(x, y, w, h):
    img = ImageGrab.grab((x, y, x + w, y + h))
    return img


def makeImageBlur(img, radius=5):
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def mergeImage(a: Image, b: Image):
    return Image.alpha_composite(a, b)

def makeImageMask(size, color=(0, 0, 0, 128), ):
    return Image.new("RGBA", size=size, color=color)

def loadFont(fontPath, FONT_LIST):
    if not fontPath in FONT_LIST:
        FONT_LIST.append(fontPath)
        maliang.toolbox.load_font(fontPath, private=True)  # must be private.

    return FONT_LIST

def testConnection():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=5)
        return True
    except Exception as e:
        return False
    
def getRelFromAbs(x, y, root):
    return (x + root.winfo_x(), y + root.winfo_y())