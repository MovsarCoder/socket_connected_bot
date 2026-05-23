from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.builder import make_row_inline_keyboards_url
from bot.keyboards.layouts import info_keyboard

router = Router()

@router.message(F.text == '👨‍💻 Тех. Поддержка.')
async def tech_support_func(message: Message):
    await message.answer("This Bot Support Info: \n", reply_markup=make_row_inline_keyboards_url(info_keyboard))
