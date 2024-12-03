from aiogram import Router, F
from aiogram.types import Message
from keyboard.kbBuilder import make_row_inline_keyboards_url

router = Router()

@router.message(F.text == '👨‍💻 Тех. Поддержка.')
async def tech_support_func(message: Message):
    https_url = "https://t.me/"

    keyboard = [
        ("Технический администратор", f"{https_url}timaadev"),
        ("Предложения и идеи", f"{https_url}timaadev"),
        ("Владелец бота", f"{https_url}timaadev"),
    ]

    await message.answer("This Bot Support Info: \n", reply_markup=make_row_inline_keyboards_url(keyboard))