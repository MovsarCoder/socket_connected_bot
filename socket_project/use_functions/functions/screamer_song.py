import os

from playsound import playsound


def play_sound(file_path):
    if os.path.exists(file_path):
        try:
            playsound(file_path)
            print("Файл воспроизведен успешно.")
        except Exception as e:
            print(f"Ошибка при воспроизведении: {e}")
    else:
        print(f"Файл {file_path} не найден.")


