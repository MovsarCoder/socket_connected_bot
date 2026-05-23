import os
import platform

def toggle_mute():
    current_os = platform.system()

    if current_os == "Windows":
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        is_muted = volume.GetMute()
        volume.SetMute(not is_muted, None)

    elif current_os == "Darwin":  # macOS
        os.system("osascript -e 'set volume output muted (not (output muted of (get volume settings)))'")

    elif current_os == "Linux":
        os.system("amixer set Master toggle")

    else:
        print("Unsupported OS")


