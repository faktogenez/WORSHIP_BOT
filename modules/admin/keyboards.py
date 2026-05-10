from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_admin_keyboard(volume=100):
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"▶️ СТАРТ"), KeyboardButton(text=f"⏹️ СТОП"), KeyboardButton(text=f"🔊 {volume}%")],
            [KeyboardButton(text="📜 ПЛЕЙЛИСТ"), KeyboardButton(text="🔄 ОБНОВИТЬ")],
            [KeyboardButton(text="📖 ПОСЛАНИЯ"), KeyboardButton(text="📊 СТАТИСТИКА")]
        ],
        resize_keyboard=True
    )
