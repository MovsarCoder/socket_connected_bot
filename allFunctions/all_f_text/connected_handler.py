import asyncio
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from States.State import Reg
import socket
from keyboard.kbBuilder import make_row_inline_keyboards

router = Router()
global_data_store = {}


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


@router.callback_query(F.data == 'connect_data')
async def connect_data(callback: CallbackQuery):
    await callback.message.answer("Ожидайте, идет подключение..")
    await asyncio.sleep(10)
    await callback.message.answer('Вы успешно подключились!')


@router.message(Reg.connected_port)
async def connected_port(message: Message, state: FSMContext):
    get_port = message.text

    if await check_input_type(get_port):
        await state.update_data(port=get_port)
        get_data = await state.get_data()

        # Сохраняем данные в глобальном словаре
        global_data_store[message.from_user.id] = {
            "IP": f"{get_data['ip']}",
            "PORT": f"{get_data['port']}",
        }

        data_info = global_data_store[message.from_user.id]

        keyboard = [
            ("Подключиться", "connect_data"),
            ("Отмена", "back_data")
        ]

        await message.answer(f'IP: {data_info.get("IP")}\nPORT: {data_info.get("PORT")}', reply_markup=make_row_inline_keyboards(keyboard))

        # Не очищаем состояние здесь, оставляем его для обработки callback
        # await state.clear()

    else:
        await message.answer('Введите полученный 4-х значный порт. (0000):')
        await state.set_state(Reg.connected_port)


# Пример использования глобальных данных в другом обработчике
@router.callback_query(F.data == 'connect_data')
async def connect_data(callback: CallbackQuery):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    user_id = callback.from_user.id

    if user_id in global_data_store:
        data_info = global_data_store[user_id]
        await callback.message.answer(f"Подключение к {data_info['IP']} на порту {data_info['PORT']}...")

        await asyncio.sleep(10)  # Симуляция процесса подключения
        await callback.message.answer('Вы успешно подключились!')
        client.connect((data_info['IP'], data_info['PORT']))
    else:
        await callback.message.answer('Данные подключения недоступны. Пожалуйста, попробуйте снова.')
