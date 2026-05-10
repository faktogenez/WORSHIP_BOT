from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from modules.admin.keyboards import get_main_admin_keyboard
from modules.utils import get_radio_status
from datetime import datetime
from bot_db import get_verse_by_date, get_verse_count, get_stats

ADMIN_ID = 468021908

admin_router = Router()

@admin_router.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("⛔ Доступ запрещён")
        return
    _, volume = await get_radio_status()
    await message.answer(
        "🛠️ *Админ панель*",
        parse_mode="Markdown",
        reply_markup=get_main_admin_keyboard(volume)
    )

@admin_router.message(F.text == "📖 ПОСЛАНИЯ")
async def bible_message(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    today = datetime.now().strftime("%Y-%m-%d")
    verse = get_verse_by_date(today)
    if verse:
        title, content, prayer = verse
        text = f"📖 *{title}*\n\n{content}\n\n🙏 *МОЛИТВА*\n{prayer}"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="📤 Опубликовать в канал", callback_data="publish_verse")]])
        await message.answer(text, parse_mode="Markdown", reply_markup=keyboard)
    else:
        await message.answer("❌ Сегодняшнего послания нет")

@admin_router.message(F.text == "📊 СТАТИСТИКА")
async def statistics(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    is_playing, volume = await get_radio_status()
    total_verses = get_verse_count()
    last_sent = get_stats("last_bible_sent") or "Нет данных"
    import json
    from pathlib import Path
    playlist_file = Path(__file__).parent.parent.parent / "playlist.json"
    songs_count = len(json.load(open(playlist_file))) if playlist_file.exists() else 0
    await message.answer(
        f"📊 *СТАТИСТИКА*\n\n"
        f"📖 Посланий в БД: {total_verses}\n"
        f"🕐 Последняя отправка: {last_sent}\n"
        f"🎵 Хвал в плейлисте: {songs_count}\n"
        f"▶️ Сейчас играет: {'Да' if is_playing else 'Нет'}\n"
        f"🔊 Громкость: {volume}%",
        parse_mode="Markdown"
    )

@admin_router.callback_query(F.data == "publish_verse")
async def publish_verse(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Доступ запрещён")
        return
    from config import DEFAULT_CHANNEL
    today = datetime.now().strftime("%Y-%m-%d")
    verse = get_verse_by_date(today)
    if verse:
        title, content, prayer = verse
        text = f"📖 *{title}*\n\n{content}\n\n🙏 *МОЛИТВА*\n{prayer}"
        await callback.bot.send_message(DEFAULT_CHANNEL, text, parse_mode="Markdown")
        await callback.answer("✅ Послание опубликовано в канал!")
        from bot_db import update_stats
        update_stats("last_bible_sent", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        await callback.answer("❌ Нет послания для публикации", show_alert=True)
