from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    connected_ip = State()
    connected_port = State()


class Form(StatesGroup):
    connected = State()


class Admin(StatesGroup):
    new_admin = State()
    remove_admin = State()
    add_new_group_name = State()
    add_new_group_username = State()
    delete_group = State()
