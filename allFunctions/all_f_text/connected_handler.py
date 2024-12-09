from keyboard.list_keyboards_info import connected_keyboard, keyboard_control_pc, keyboard_check_is_control, keyboard_control_youtube
from keyboard.kbBuilder import make_row_inline_keyboards
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from States.State import Reg
import socket

router = Router()
global_data_store = {}
client = None

"""
# @router.message(Form.connected)
# async def send_message(message: Message, ):
#     global client
#     if client:
#         try:
#             client.send(message.text.encode())
#             await message.answer(f'Сообщение отправлено: {message.text}')
#         except Exception as e:
#             await message.answer(f'Ошибка при отправке сообщения: {e}')
#     else:
#         await message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')
"""


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
            client.send("shutdown".encode())
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
            client.send('restart'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')


@router.callback_query(F.data == 'blue_screen_of_dead')
async def blue_screen(callback: CallbackQuery):
    """
    Данная функция отправляет сообщение на компьютер к которому мы подключились с помощью сокетов.
     Функция называется bsod_browser (Синий экран смерти (blue_dead_screen)).
      На стороне клиента эта функция уже обрабатывает функцию вызова шуточного синего экрана смерти компьютера.
      Тем самым мы можем удаленно вызвать шуточный синий экран смерти компьютера, любого человека.
    """
    await callback.answer('')
    global client

    if client:
        try:
            await callback.message.answer('Синий экран вызван успешно!')
            client.send('bsod_browser'.encode())
        except Exception as e:
            await callback.message.answer(f'Ошибка при отправке сообщения: {e}')
    else:
        await callback.message.answer('Сначала подключитесь к серверу с помощью команды кнопки "🔛 Подключиться к 🖥️".')





################################################################## Все функции для управления Youtube


# Клавиатура с функционалом для управления Youtube
@router.callback_query(F.data == 'control_youtube')
async def control_youtube_keyboard(callback: CallbackQuery):
    """

    :param callback:
    :return:
    """
    await callback.answer('')

    await callback.message.edit_text('Доступный функционал использования программы Youtube: ', reply_markup=make_row_inline_keyboards(keyboard_control_youtube))


# Функция для открытия Youtube
@router.callback_query(F.data == 'open_youtube_data')
async def open_youtube_func(callback: CallbackQuery):
    """

    :param callback:
    :return:
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
