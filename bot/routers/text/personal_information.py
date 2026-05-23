from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.services.database import selectToTable

router = Router()

@router.message(Command('profile'))
@router.message(F.text == 'ℹ️ Личная информация')
async def personal_information_func(message: Message):
    id_user = message.from_user.id
    get_id_user = selectToTable(id_user)
    get_id_user_info = \
        {
            "name": get_id_user.get("name"),
                "firstname": get_id_user.get('firstname'),
                    "lastname": get_id_user.get('lastname'),
                        "sign_up_people": get_id_user.get('sign_up_people'),
                            "telegram_id": get_id_user.get('telegram_id'),
                                "unique_id": get_id_user.get('unique_id'),
        }

    send_info_message = f"""
    📊 Статистика пользователя\n
    
    Подписка: стандартная ✔️
    Выбрана модель: <N/A> - ?\n
    
        ℹ️ Личная информация по пользователю "{get_id_user_info.get("name")}" \n
            👨 Имя пользователя: {get_id_user_info.get("firstname")} 
                👨 Фамилия пользователя (Если имеется): {get_id_user_info.get("lastname")}
                    👨 Дата регистрации в боте: {get_id_user_info.get("sign_up_people")}
                        👨 Ваш уникальный идентификатор Telegram (ID): {get_id_user_info.get("telegram_id")}
                            👨 Ваш уникальный идентификатор (ID): {get_id_user_info.get("unique_id")}
    
    
    """
    await message.answer(send_info_message)
