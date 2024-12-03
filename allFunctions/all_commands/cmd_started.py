from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from allFunctions.functions.generate_uqinue_id import generate_password
from database.db import insertIntoToTable, user_exists
import datetime
from keyboard.kbBuilder import make_row_keyboards

router = Router()


@router.message(StateFilter(None), Command('start'))
async def get_name_func(message: Message, state: FSMContext):
    await state.clear()
    id_player = message.from_user.id

    # Список из всех доступных кнопок
    keyboard = [
        'ℹ️ Личная информация',
        '⚙️ Моя OC (Операционная Система)',
        '👨‍💻 Тех. Поддержка.',
        '📝 Получить Builder',
        '📴 Закрыть соединение с 🖥️', '🔛 Подключиться к 🖥️'
    ]

    # Проверяем, существует ли пользователь в базе данных
    if user_exists(id_player):
        await message.reply("Привет. У нас все как обычно! Список всех доступных функций бота /help", reply_markup=make_row_keyboards(keyboard))
        return  # Если пользователь уже существует, ничего не делаем

    # Если пользователь не существует в базе данных
    else:
        # Переменная для определения времени на момент запуска бота (первого старта).
        start_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        generate_unique_id = generate_password()
        dict_case = \
            {
                'name': message.from_user.full_name,
                'firstname': message.from_user.first_name,
                'lastname': message.from_user.last_name,
                'sign_up_people': start_time,
                'telegram_id': id_player,
                'unique_id': generate_unique_id
            }

        (insertIntoToTable
            (
            dict_case.get("name"),
            dict_case.get("firstname"),
            dict_case.get("lastname"),
            dict_case.get("sign_up_people"),
            dict_case.get("telegram_id"),
            dict_case.get('unique_id'),
        )
        )

        await message.reply("Привет! Добро пожаловать в наш бот! Вы походу у нас в первые. \n Список всех доступных функций бота /help", reply_markup=make_row_keyboards(keyboard))

# @router.message(Reg.email)
# async def get_email_func_fsm(message: Message, state: FSMContext):
#     await state.update_data(email=message.text)
#     await message.answer('Отлично! Мы приняли ваши данные!')
#     await state.clear()
#     # await get_text(message, state)
#
#
# async def get_text(message: Message, state: FSMContext):
#     get_info = await state.get_data()
#     data = {
#         'email': f'{get_info.get("email")}',
#         'name': f'{get_info.get("name")}',
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             data[item.type] = item.extract_from(message.text)
#
#     await message.reply('Вот что я нашел: \n'
#                         f'E-mail: {html.quote(data["email"])}\n'
#                         f'Пароль: {html.quote(data["name"])}'
#                         )
