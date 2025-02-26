import os
import pwd
import subprocess
from pathlib import Path

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
    common_paths = [
        Path.home() / ".face",
        Path.home() / ".face.icon",
        Path(f"/var/lib/AccountsService/icons/{user}"),
        Path.home() / ".config/accountsservice/icons" / user
    ]
    if de == "gnome":
        common_paths += [
            Path.home() / ".config/gnome/accountsservice/users/" / user
        ]
    elif de == "kde":
        common_paths += [
            Path.home() / ".config/kdeglobals"
        ]
    for path in common_paths:
        if path.exists():
            if path.is_file() and path.stat().st_size > 0:
                return str(path)
            elif path.is_dir():
                possible_images = list(path.glob("*.[pj][np]g"))
                if possible_images:
                    return str(possible_images[0])
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
