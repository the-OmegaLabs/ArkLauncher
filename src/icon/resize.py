from PIL import Image


icon = Image.open('src/icon/exit.png')

icon = icon.resize((128, 128), 1)


icon.save('src/icon/exit.png')