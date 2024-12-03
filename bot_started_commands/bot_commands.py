from aiogram.types import BotCommand

start_command = BotCommand(command='start', description='Запуск бота')
description_command = BotCommand(command='help', description='Доступные функции бота')
profile_command = BotCommand(command='profile', description='Профиль')

# Создаем общий список команд
commands = [start_command, description_command, profile_command]

# Устанавливаем команды
