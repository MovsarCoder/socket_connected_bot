from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def cmd_help(message: Message):
    a = """
    Все доступные функции бота: \n
    /start - Перезагрузка бота \n
    /help - Информация о боте \n
    /profile - Ваша личная информация \n
    /admin_panel - Админ панель \n
    """
    await message.answer(a)
