import os
import ctypes
from shutil import copyfile

def install_font(font_path):
    if not os.path.exists(font_path):
        print(f"字体文件 {font_path} 不存在!")
        return

    # 获取字体的系统目录
    system_fonts_dir = os.path.join(os.environ['WINDIR'], 'Fonts')

    # 获取字体文件的文件名
    font_name = os.path.basename(font_path)

    # 复制字体文件到系统字体目录
    copyfile(font_path, os.path.join(system_fonts_dir, font_name))

    # 调用AddFontResourceEx方法添加字体
    ctypes.windll.gdi32.AddFontResourceExW(os.path.join(system_fonts_dir, font_name), 0, None)

    # 刷新系统字体缓存
    ctypes.windll.user32.SendMessageW(0x0000, 0x001D, 0, 0)

    print(f"字体 {font_name} 安装成功!")

# 传入字体文件路径
install_font(r"C:\Users\Stevesuk\Desktop\ArkLauncher2\src\font.ttf")
