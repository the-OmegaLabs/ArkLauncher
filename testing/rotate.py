import tkinter as tk


def on_focus_in(event):
    event.widget.config(bg="lightblue")  # 聚焦时改变按钮背景色
    print("按钮获得焦点")


def on_focus_out(event):
    event.widget.config(bg="SystemButtonFace")  # 恢复默认背景色
    print("按钮失去焦点")


root = tk.Tk()
button = tk.Button(root, text="测试按钮")
button.pack(padx=20, pady=20)

# 绑定事件
button.bind("<FocusIn>", on_focus_in)
button.bind("<FocusOut>", on_focus_out)

root.mainloop()
