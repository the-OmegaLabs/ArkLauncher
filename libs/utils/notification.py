import libs.utils.systemDetector as sd
import libs.values.values as val
if sd.get_windows_version()==11:
    import win11toast as toast
else:
    import win10toast as toast

def create_notification(text: str, icon: val.NotificationIcon, duration: int = 5):
    toast.ToastNotifier().show_toast(
        "ArkLauncher",
        text,
        icon_path=icon.getImagePath(),
        duration=duration
    )