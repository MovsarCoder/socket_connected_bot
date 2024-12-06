import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from States.State import Reg
import socket
from keyboard.kbBuilder import make_row_inline_keyboards
from keyboard.list_keyboards_info import connected_keyboard, keyboard_control_pc, keyboard_check_is_control

router = Router()
global_data_store = {}
client = None


async def send_messages():
    while True:
        await asyncio.sleep(0.1)


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

        # Создаем список содержащий кортеж из двух элементов для дальнейшего составления inline-keyboard из этих данных
        # [("Название кнопки", "callback_data для взаимодействия с кнопкой")]

        # Получаем дату (информацию с состояний)
        get_data = await state.get_data()
        # Сохраняем данные в глобальном словаре
        global_data_store[message.from_user.id] = {
            "ip": f"{get_data['ip']}",
            "port": int(get_data['port']),  # Преобразуем порт в целое число
        }

        data_info = global_data_store[message.from_user.id]
        await message.answer(f'IP: {data_info.get("ip")}\nPORT: {data_info.get("port")}', reply_markup=make_row_inline_keyboards(connected_keyboard))

        # Не очищаем состояние здесь, оставляем его для обработки callback
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

        # Имитируем подключение к серверу
        await asyncio.sleep(5)

        # Если данные успешны, то подключаемся
        try:
            # Подключение по сокетам к IP
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((data_info.get('ip'), data_info.get('port')))
            await callback.message.edit_text('Вы успешно подключились!', reply_markup=make_row_inline_keyboards(keyboard_check_is_control))
            # Устанавливаем состояние
            # await state.set_state(Form.connected)
        # При возникновении непредвиденных ошибок
        except Exception as e:
            await callback.message.edit_text(f'Ошибка подключения: {e}')
    # Если данные не успешны, вызываем ошибку
    else:
        await callback.message.edit_text('Данные подключения недоступны. Пожалуйста, попробуйте снова.')


@router.callback_query(F.data == 'control_pc')
async def control_pc_func(callback: CallbackQuery):
    # Выключаем свечение кнопки
    await callback.answer('')
    # Создаем список из кортежей с кнопками и датами
    # asyncio.create_task(send_messages())

    # Редактируем прошлую клавиатуру на новую
    await callback.message.edit_text('Успешно! Доступный функционал компьютера: ', reply_markup=make_row_inline_keyboards(keyboard_control_pc))


@router.callback_query(F.data == 'shutdown_data')
async def shutdown_data(callback: CallbackQuery):
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

# @router.message(F.text == "📴 Закрыть соединение с 🖥️")
# async def disconnect_handler(message: Message, state: FSMContext):
#     await state.clear()
#     global client
#     if client:
#         client.close()
#         await message.answer('Вы отключены от сервера.')
#         await state.clear()  # Завершаем состояние
#     else:
#         await message.answer('Вы не подключены к серверу.')
