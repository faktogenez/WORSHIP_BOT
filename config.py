import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

# === 1. ДАННЫЕ БОТА (для уведомлений и рассылок) ===
BOT_TOKEN = os.getenv("BOT_TOKEN")

# === 2. ДАННЫЕ USERBOT (Аккаунта-ведущего) ===
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
# В .env нужно добавить номер телефона аккаунта
USERBOT_PHONE = os.getenv("USERBOT_PHONE")  # Например: +79991234567

# === 3. НАСТРОЙКИ ===
ADMIN_ID = int(os.getenv("ADMIN_ID"))          # Ваш личный ID
DEFAULT_CHANNEL = int(os.getenv("DEFAULT_CHANNEL", -1001990792121)) # Числовой ID канала
TIMEZONE = os.getenv("TIMEZONE", "Europe/Moscow")

# === 4. РАДИО СТАНЦИИ ===
RADIO_STREAMS = {
    "radio1": {
        "name": "Moses Bliss - MERCY",
        "path": str(BASE_DIR / "music" / "mercy.mp3")
    },
    "radio2": {
        "name": "Вторая станция",
        "path": str(BASE_DIR / "music" / "test.mp3")
    }
}