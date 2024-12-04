from aiogram.fsm.state import State, StatesGroup
class Reg(StatesGroup):
    connected_ip = State()
    connected_port = State()

class Form(StatesGroup):
    connected = State()


# name = State()
# id_player = State()
# fisrt_name = State()
# sign_up_people = State()
# last_name = State()
# email = State()
# telephone = State()