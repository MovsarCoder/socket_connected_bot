from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")
TELEGRAM_ID = os.getenv("TELEGRAM_ID")