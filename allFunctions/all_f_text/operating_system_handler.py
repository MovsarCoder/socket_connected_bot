import platform
import time

from aiogram import F, Router
from aiogram.types import Message
import psutil

router = Router()


@router.message(F.text == '⚙️ Моя OC (Операционная Система)')
async def get_info_oc(message: Message):
    info = {
        "Система": platform.system(),
        "Имя узла": platform.node(),
        "Версия": platform.release(),
        "Полная версия": platform.version(),
        "Архитектура": platform.architecture()[0],
        "Тип машины": platform.machine(),
        "Процессор": platform.processor(),
    }

    # Форматируем сообщение
    formatted_info = "\n".join([f"<b>{key}:</b> {value}" for key, value in info.items()])

    await message.answer(f'⚙️ Моя OC (Операционная Система) \n\n{formatted_info}', parse_mode='HTML')


    # Состояние комплектующих
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    uptime_seconds = int(psutil.boot_time())
    uptime = str(psutil.boot_time())

    uptime = int(time.time() - uptime_seconds)
    hours, remainder = divmod(uptime, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_formatted = f"{hours} ч {minutes} мин {seconds} сек"
    await message.answer('"📊 **Информация о системе:**\n\n**CPU:** {cpu_usage}%\n**Память:** {memory_usage}%\n**Аптайм:** {uptime_formatted}"')
