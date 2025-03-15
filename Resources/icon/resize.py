from PIL import Image


icon = Image.open('Resources/icon/exit.png')

icon = icon.resize((128, 128), 1)


icon.save('Resources/icon/exit.png')
