import pygetwindow as gw
import pyautogui
import time

def toggle_youtube_video():
    # Получаем список всех открытых окон
    windows = gw.getAllTitles()

    # Проверяем наличие YouTube в заголовках окон
    for window in windows:
        if "YouTube" in window:
            # Активируем окно браузера
            browser_window = gw.getWindowsWithTitle(window)[0]
            browser_window.activate()
            time.sleep(1)  # Ждем, чтобы окно активировалось

            # Пытаемся нажать пробел для остановки или воспроизведения видео
            pyautogui.press('space')
            return

    print("YouTube не найден в открытых окнах.")

