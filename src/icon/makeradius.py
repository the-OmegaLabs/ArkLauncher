from PIL import Image, ImageDraw

img = Image.open('src/icon/contributors/HRGC-Sonrai.jpg').convert("RGBA")

mask = Image.new("L", img.size, 0)
draw = ImageDraw.Draw(mask)

draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=20, fill=255)

img.putalpha(mask)

img.show() 
img.save("src/icon/contributors/Xiaokang2022.png") 
