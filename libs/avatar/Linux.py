import os
import pwd
import subprocess

import libs.olog as olog


def detect_desktop_environment():
    de = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if de:
        if "gnome" in de:
            return "gnome"
        elif "kde" in de:
            return "kde"
        elif "xfce" in de:
            return "xfce"
    try:
        ps_output = subprocess.check_output(["ps", "-e"]).decode()
        if "gnome-session" in ps_output:
            return "gnome"
        elif "plasmashell" in ps_output:
            return "kde"
        elif "xfce4-session" in ps_output:
            return "xfce"
    except Exception:
        pass
    return "unknown"


def get_user_avatar_path(de):
    user = pwd.getpwuid(os.getuid()).pw_name
    home_dir = os.path.expanduser('~')
    common_paths = [
        os.path.join(home_dir, ".face"),
        os.path.join(home_dir, ".face.icon"),
        os.path.join("/var/lib/AccountsService/icons", user),
        os.path.join(home_dir, ".config/accountsservice/icons", user)
    ]
    if de == "gnome":
        common_paths.append(os.path.join(
            home_dir, ".config/gnome/accountsservice/users", user))
    elif de == "kde":
        common_paths.append(os.path.join(home_dir, ".config/kdeglobals"))

    for path in common_paths:
        if os.path.exists(path):
            if os.path.isfile(path) and os.path.getsize(path) > 0:
                return path
            elif os.path.isdir(path):
                possible_images = []
                for f in os.listdir(path):
                    if f.lower().endswith(('.png', '.jpg')):
                        possible_images.append(os.path.join(path, f))
                if possible_images:
                    return possible_images[0]
    return None


def getAvatar():
    de = detect_desktop_environment()
    avatar_path = get_user_avatar_path(de)
    olog.output(f"Desktop Environment: {de}")
    """ 用不了：
    PIL.UnidentifiedImageError: cannot identify image file '/home/stevesuk/.face'

    if avatar_path:
        return avatar_path
    else:
    """
    return "src/Contributors/Stevesuk0.jpg"
