import platform
from aiogram import F, Router
from aiogram.types import Message

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
