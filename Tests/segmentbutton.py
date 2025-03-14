import maliang
root = maliang.Tk()
cv = maliang.Canvas(root)
cv.pack()
maliang.SegmentedButton(cv, (0, 0), text=(
    'hello', 'maliang', '123456'), command=lambda x: print(x), default=2)
root.mainloop()
