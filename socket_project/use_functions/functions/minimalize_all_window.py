import ctypes

def minimize_all_windows_func():
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x4D, 0, 0, 0)
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
    ctypes.windll.user32.keybd_event(0x4D, 0, 2, 0)
    print('Все окна успешно свернуты!')
