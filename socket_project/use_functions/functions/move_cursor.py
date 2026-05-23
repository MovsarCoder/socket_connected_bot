import random
import threading
import time
import pyautogui
import platform

cursor_moving = False
cursor_thread = None


# Создаем функцию, которая перемещает курсор в случайное место.
def move_cursor_randomly():
    global cursor_moving
    screen_width, screen_height = pyautogui.size()  # Размеры экрана

    while cursor_moving:
        # Генерация случайных координат (x, y)
        x = random.randint(0, screen_width)
        y = random.randint(0, screen_height)

        # Перемещаем курсор с учетом совместимости с разными платформами.
        pyautogui.moveTo(x, y, duration=0.5)
        time.sleep(1)


# Запуск случайного перемещения курсора.
def start_moving_cursor():
    global cursor_moving, cursor_thread

    # Проверка текущей платформы
    current_system = platform.system()
    if current_system not in ["Windows", "Linux", "Darwin"]:
        print(f"Эта платформа не поддерживается: {current_system}")
        return

    if cursor_moving:
        print("Курсор уже перемещается.")
        return

    cursor_moving = True
    cursor_thread = threading.Thread(target=move_cursor_randomly, daemon=True)
    cursor_thread.start()
    print(f"Случайное перемещение курсора начато на {current_system}.")


# Останавливает случайное перемещение курсора.
def stop_moving_cursor():
    global cursor_moving
    cursor_moving = False  # Останавливаем фоновую задачу
    print("Случайное перемещение курсора завершено.")
