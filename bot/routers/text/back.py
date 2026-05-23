from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.builder import make_row_inline_keyboards
from bot.keyboards.layouts import keyboard_check_is_control

router = Router()


@router.callback_query(F.data == 'back_data')
async def back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        await callback.message.edit_text('Выберите функцию', reply_markup=make_row_inline_keyboards(keyboard_check_is_control))

    except Exception as e:
        await callback.message.answer('Произошла непредвиденная ошибка')
