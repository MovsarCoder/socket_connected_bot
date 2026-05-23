# SocketHasskelConnectBot

## Структура

- `bot/` — Telegram-бот: роутеры, клавиатуры, FSM-состояния, сервисы базы и админ-хранилища.
- `socket_server/` — socket-сервер и действия, которые он выполняет по командам от бота.
- `core/` — общий конфиг проекта, пути к данным и переменные окружения.
- `data/` — SQLite-база и JSON/TXT-хранилища бота.
- `run_bot.py` — запуск Telegram-бота.
- `run_socket_server.py` — запуск socket-сервера.

## Переменные окружения

Все переменные теперь читаются из корневого `.env`:

```env
BOT_TOKEN=
SOCKET_BOT_TOKEN=
TELEGRAM_ID=
EMAIL_SENDER=
EMAIL_RECEIVER=
EMAIL_PASSWORD=
```

`SOCKET_BOT_TOKEN` нужен для отправки файлов из socket-сервера в Telegram. Если он не задан, используется `TOKEN`, а затем `BOT_TOKEN`.
`EMAIL_*` используется socket-сервером для отправки уведомлений о подключении.

## Запуск

```bash
python3 run_bot.py
python3 run_socket_server.py
```
