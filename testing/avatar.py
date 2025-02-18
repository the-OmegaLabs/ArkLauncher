import os
from PIL import Image

username = os.environ.get('USERNAME')

account_pictures_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\AccountPictures"

# 获取目录下所有图片文件并按修改时间排序
image_files = []
for filename in os.listdir(account_pictures_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_path = os.path.join(account_pictures_dir, filename)
        image_files.append((file_path, os.path.getmtime(file_path)))

# 选择最新修改的文件（假设为当前头像）
if image_files:
    latest_image = max(image_files, key=lambda x: x[1])[0]
    img = Image.open(latest_image)
    img.show()
else:
    print("未找到用户头像文件")