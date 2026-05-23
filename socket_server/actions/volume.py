import platform
import os



def set_max_volume():
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            os.system("osascript -e 'set volume output volume 100'")
            print("Громкость установлена на максимум на macOS.")
        except Exception as e:
            print(f"Произошла ошибка на macOS: {e}")

    elif system == "Linux":
        try:
            os.system("pactl set-sink-volume @DEFAULT_SINK@ 100%")
            print("Громкость установлена на максимум на Linux.")
        except Exception as e:
            print(f"Произошла ошибка на Linux: {e}")

    elif system == "Windows":
        # Импорты только для Windows
        import ctypes
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from comtypes import CLSCTX_ALL
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevel(volume.GetVolumeRange()[1], None)
            print("Громкость установлена на максимум на Windows.")
        except Exception as e:
            print(f"Произошла ошибка на Windows: {e}")

    else:
        print("Эта операционная система не поддерживается.")

