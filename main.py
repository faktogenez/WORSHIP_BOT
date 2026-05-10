import asyncio
import os
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from telethon import TelegramClient

from config import BOT_TOKEN, ADMIN_ID, DEFAULT_CHANNEL, API_ID, API_HASH
from bot_db import init_db, get_verse_by_date
from scheduler_bible import setup_bible_scheduler

from modules import admin_router, radio_router

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(admin_router)
dp.include_router(radio_router)

def get_main_keyboard(is_admin=False):
    buttons = [[KeyboardButton(text="📖 Послание дня")]]
    if is_admin:
        buttons.append([KeyboardButton(text="🛠️ Админ панель")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(Command("start"))
async def start_command(message: Message):
    is_admin = (message.from_user.id == ADMIN_ID)
    await message.answer(
        "🙏 Добро пожаловать в Христианский Бот!\n\nИспользуйте кнопки ниже:",
        reply_markup=get_main_keyboard(is_admin)
    )

@dp.message(F.text == "📖 Послание дня")
async def verse_button(message: Message):
    today = datetime.now().strftime("%Y-%m-%d")
    verse = get_verse_by_date(today)
    
    if verse:
        title, content, prayer = verse
        response = f"📖 *{title}*\n\n{content}\n\n🙏 *МОЛИТВА*\n{prayer}"
    else:
        response = "📖 Сегодняшнего послания ещё нет в базе."
    
    await message.answer(response, parse_mode="Markdown")

@dp.message(F.text == "🛠️ Админ панель")
async def admin_button(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Доступ запрещён")
        return
    await message.answer("🛠️ Админ панель\n/admin для управления")

async def main():
    init_db()
    logger.info("Database initialized")
    
    setup_bible_scheduler(bot, DEFAULT_CHANNEL)
    logger.info(f"Scheduler configured for {DEFAULT_CHANNEL}")
    
    userbot = TelegramClient('admin_session', API_ID, API_HASH)
    await userbot.start()
    me = await userbot.get_me()
    logger.info(f"Userbot client установлен, ID: {me.id}")
    
    print("\n" + "="*50)
    print("🤖 ХРИСТИАНСКИЙ БОТ ЗАПУЩЕН")
    print("="*50)
    print(f"👑 Админ ID: {ADMIN_ID}")
    print(f"📢 Канал: {DEFAULT_CHANNEL}")
    print("="*50 + "\n")
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
