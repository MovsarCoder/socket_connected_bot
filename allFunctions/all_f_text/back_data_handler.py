from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboard.kbBuilder import make_row_inline_keyboards
from keyboard.list_keyboards_info import keyboard_check_is_control

router = Router()

@router.callback_query(F.data == 'back_data')
async def back(callback: CallbackQuery):
    try:
        await callback.message.edit_text('Выберите функцию', reply_markup=make_row_inline_keyboards(keyboard_check_is_control))

    except Exception as e:
        await callback.message.answer('Произошла непредвиденная ошибка')