import tkinter as tk
import ctypes
from ctypes import wintypes

# Windows API常量
GWL_WNDPROC = -4
WM_DROPFILES = 0x0233
WM_DESTROY = 0x0002
WM_CREATE = 0x0001

# 加载Windows函数
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
shell32 = ctypes.windll.shell32

# Drop handler
def low_level_drop(hwnd, msg, wparam, lparam):
    if msg == WM_DROPFILES:
        n_files = shell32.DragQueryFileW(wparam, 0xFFFFFFFF, None, 0)
        for i in range(n_files):
            length = shell32.DragQueryFileW(wparam, i, None, 0)
            buffer = ctypes.create_unicode_buffer(length + 1)
            shell32.DragQueryFileW(wparam, i, buffer, length + 1)
            filepath = buffer.value
            # 读取文件内容插入到文本框
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                text.insert(tk.END, content + "\n")
            except Exception as e:
                text.insert(tk.END, f"[Failed to read {filepath}: {e}]\n")
        shell32.DragFinish(wparam)
        return 0
    return user32.CallWindowProcW(old_wndproc, hwnd, msg, wparam, lparam)

# 创建新的WndProc回调
WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_long, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)

def set_window_proc(hwnd):
    global new_wndproc
    new_wndproc = WNDPROCTYPE(low_level_drop)
    return user32.SetWindowLongPtrW(hwnd, GWL_WNDPROC, new_wndproc)

# 创建Tk窗口
root = tk.Tk()
root.title('Drag Text File Here')
root.geometry('500x400')

text = tk.Text(root, wrap="word")
text.pack(expand=True, fill="both")

root.update()  # 更新窗口，拿到正确的句柄

# 获取窗口句柄
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

# 允许窗口接受拖拽
shell32.DragAcceptFiles(hwnd, True)

# 替换窗口过程
old_wndproc = user32.GetWindowLongPtrW(hwnd, GWL_WNDPROC)
set_window_proc(hwnd)

root.mainloop()
