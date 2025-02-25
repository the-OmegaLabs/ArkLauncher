import getpass
import os

username = getpass.getuser()


def getAvatar():
    account_pictures_dir = f"C:\\Users\\{username}\\AppData\\Roaming\\Microsoft\\Windows\\AccountPictures"

    image_files = []
    for filename in os.listdir(account_pictures_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(account_pictures_dir, filename)
            image_files.append((file_path, os.path.getmtime(file_path)))

    if image_files:
        return max(image_files, key=lambda x: x[1])[0]
    elif os.path.exists("C:\\ProgramData\\Microsoft\\User Account Pictures\\user.png"):
        return "C:\\ProgramData\\Microsoft\\User Account Pictures\\user.png"
    else:
        return "src/Contributors/Stevesuk0.jpg"
