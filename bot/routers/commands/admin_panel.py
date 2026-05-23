from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards.builder import *
from bot.keyboards.layouts import back_keyboard, admin_keyboard
from bot.services.admin_storage import *
from bot.states.state import *

router = Router()


@router.message(Command("admin_panel"))
@router.message(F.text == '🛠️ Админ панель')
async def admin_panel_router(message: Message):
    admin_users_list = checked_admin_list()
    if message.from_user.id in admin_users_list:
        await message.answer('Выберите действие', reply_markup=make_row_inline_keyboards(admin_keyboard))
    else:
        await message.answer(f'{message.from_user.full_name}({message.from_user.id}) вы не можете получить доступ к Admin функциям данного бота! Так как не являетесь Admin!')


@router.callback_query(F.data == 'new_admin_data')
async def new_admin_user_func(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите ID пользователя, которого хотите добавить как админ', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(Admin.new_admin)


@router.message(Admin.new_admin)
async def add_admin_id(message: Message, state: FSMContext):
    await state.update_data(id=message.text)
    try:
        a = add_new_admin_db(message.text)
        # Добавляем ID пользователя в список администраторов
        if a:
            # print('Администратор был успешно добавлен в базу данных')
            await message.answer(f'Пользователь с ID {message.text} добавлен как админ.', reply_markup=make_row_inline_keyboards(admin_keyboard))
            await state.clear()
        # Не удалось найти пользователя по данному ID
        else:
            await message.answer('Не удалось найти пользователя по этому ID или уже существует такой Администратор!', reply_markup=make_row_inline_keyboards(admin_keyboard))
    except ValueError as e:
        await message.answer(f'Ошибка добавления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_keyboard))


@router.callback_query(F.data == 'remove_admin_list_data')
async def remove_admin_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Введите ID пользователь, которого хотите удалить', reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(Admin.remove_admin)


@router.message(Admin.remove_admin)
async def remove_admin(message: Message, state: FSMContext):
    try:
        if remove_admin_from_db(message.text):
            # Администратор успешно удален из базы данных.
            await message.answer(f'Пользователь с ID {message.text} был удален!', reply_markup=make_row_inline_keyboards(admin_keyboard))
            await state.clear()
        else:
            # Не удалось найти администратора в базе данных.
            await message.answer('Не удалось найти администратора в базе данных.', reply_markup=make_row_inline_keyboards(admin_keyboard))

    except ValueError as e:
        await message.answer(f'Ошибка удаления пользователя. Ошибка: {e}', reply_markup=make_row_inline_keyboards(admin_keyboard))


@router.callback_query(F.data == 'add_new_group_username_data')
async def add_new_group_username_db(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Отправьте username канала/группы (без использования @)!',
                                  reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(Admin.add_new_group_username)


@router.message(Admin.add_new_group_username)
async def fsm_add_new_group_username(message: Message, state: FSMContext):
    await message.answer(f'Хорошо! Username: {message.text}; Теперь отправьте название канала которое будет отображаться на кнопке!')
    await state.update_data(add_new_group_username=message.text)
    await state.set_state(Admin.add_new_group_name)


@router.message(Admin.add_new_group_name)
async def fsm_add_new_group_name(message: Message, state: FSMContext):
    await state.update_data(add_new_group_name=message.text)
    information_group = await state.get_data()

    # Сохраняем данные в JSON файл
    group_data = {
        'username': information_group['add_new_group_username'],
        'name': information_group['add_new_group_name']
    }

    # Если такая группа с таким Username присутствует, выводится данное сообщение.
    if not writer_group_to_json(group_data):
        await message.answer(f'Ошибка! Группа с таким username уже существует: {group_data["username"]}', reply_markup=make_row_inline_keyboards(admin_keyboard))
        return False

    # Если все успешно и Username свободен, группа успешно добавляется.
    await message.answer(f'Отлично! Информацию про новую группу:\nUsername: {group_data["username"]}\nName: {group_data["name"]}', reply_markup=make_row_inline_keyboards(admin_keyboard))
    await state.clear()


@router.callback_query(F.data == 'delete_group_data')
async def remove_group_db_func(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    await callback.message.answer('Send username in the remove group/chanel (dont use "@")',
                                  reply_markup=make_row_inline_keyboards(back_keyboard))
    await state.set_state(Admin.delete_group)


@router.message(Admin.delete_group)
async def fsm_remove_group_db(message: Message, state: FSMContext):
    try:
        # Переменная для ловли сообщения от пользователя
        message_text = message.text
        # Если с написанным пользователем Username присутствует, то она удалится.
        remove_func = remove_group_from_json(message_text)
        # Если функция remove_func возвращает True - группа удаляется и выводится сообщение
        if remove_func:
            await message.answer(f'Группа с Username: {message_text} успешно удалена!', reply_markup=make_row_inline_keyboards(admin_keyboard))
            await state.clear()
        # Если такой группы нет.
        else:
            await message.answer('Ошибка! Невозможно найти группу с таким Username!', reply_markup=make_row_inline_keyboards(admin_keyboard))

    except KeyError as e:
        await message.answer(f'Ошибка типа 3453-234567 - {e}!')


@router.callback_query(F.data == 'list_group_data')
async def group_list_db(callback: CallbackQuery):
    await callback.answer('')
    groups = load_from_json()
    keyboard = []

    # если в JSON-файле нет никаких групп для подписки, выведется данное сообщение
    if not groups:
        await callback.message.answer("Нет добавленных групп.", reply_markup=make_row_inline_keyboards(back_keyboard))
        return
    # если в JSON-файле есть группа из нее создастся клавиатура
    for group in groups:
        keyboard.append([InlineKeyboardButton(text=f'{group["name"]}', url=f'https://t.me/{group["username"]}')])

    # добавление кнопки "Назад" к клавиатуре чтобы вернутся к списку функций администратора.
    keyboard.append([InlineKeyboardButton(text='🔙Назад', callback_data='back_data2')])
    keyboard_list = InlineKeyboardMarkup(inline_keyboard=keyboard)

    # вывод сообщения со всеми группами и кнопкой "Назад"
    await callback.message.edit_text('Доступные группы:', reply_markup=keyboard_list)


@router.callback_query(F.data == 'back_data2')
async def back_func_2(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('')
    await callback.message.edit_text('Выберите действие', show_alert=True, reply_markup=make_row_inline_keyboards(admin_keyboard))
