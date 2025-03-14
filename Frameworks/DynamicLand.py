import maliang
import maliang.animation
import maliang.theme.manager
import tkinter as tk

# Skid from https://segmentfault.com/q/1010000042829943




# Main
def main():
    root = maliang.Tk()
    root.bind("<Button-1>",exit)
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry(position=(width//2-int(width/8),0), size=(int(width/4), int(height/5)))
    maliang.theme.manager.set_color_mode("dark")
    cv = maliang.Canvas(root)
    cv.place(width=int(width/4),height=int(height/5))
    def round_rectangle(x1, y1, x2, y2, r=25, **kwargs):
        nonlocal cv
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return cv.create_polygon(points, **kwargs, smooth=True)
    round_rectangle(0,0,int(width/4),int(height/5),r=100)
    root.mainloop()

if __name__ == "__main__":
    main()