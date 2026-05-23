import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"
DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "database.db"
ADMIN_LIST_PATH = DATA_DIR / "admin_list.txt"
GROUPS_PATH = DATA_DIR / "groups.json"
PLAYERS_LIST_PATH = DATA_DIR / "players_list_db.txt"

SOCKET_RUNTIME_DIR = BASE_DIR / "socket_server" / "runtime"
SOCKET_ASSETS_DIR = BASE_DIR / "socket_server" / "assets"
SOCKET_PHOTOS_DIR = SOCKET_RUNTIME_DIR / "photos"
SOCKET_SCREENSHOTS_DIR = SOCKET_RUNTIME_DIR / "screenshots"
SOCKET_VIDEO_DIR = SOCKET_RUNTIME_DIR / "video"

load_dotenv(ENV_PATH)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
