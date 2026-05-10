import json
import asyncio
import os
from pathlib import Path
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from modules.utils import send_http_command, get_radio_status

ADMIN_ID = 468021908
PLAYLIST_FILE = Path(__file__).parent.parent.parent / "playlist.json"

radio_router = Router()

def get_valid_playlist():
    if not PLAYLIST_FILE.exists():
        return []
    with open(PLAYLIST_FILE, 'r', encoding='utf-8') as f:
        pl = json.load(f)
    return [track for track in pl if os.path.exists(track.get('path', ''))]

@radio_router.message(F.text == "▶️ СТАРТ")
async def start_radio(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    is_playing, _ = await get_radio_status()
    if is_playing:
        await message.answer("🎵 Хвала уже играет")
        return
    result = await send_http_command("start")
    await message.answer(result.get("status", "🎵 Запуск..."))

@radio_router.message(F.text == "⏹️ СТОП")
async def stop_radio(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    is_playing, _ = await get_radio_status()
    if not is_playing:
        await message.answer("⏹️ Хвала уже остановлена")
        return
    result = await send_http_command("stop")
    await message.answer(result.get("status", "⏹️ Остановка..."))

@radio_router.message(F.text.startswith("🔊"))
async def volume_control(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    _, current_volume = await get_radio_status()
    new_volume = 15 if current_volume == 100 else 100
    result = await send_http_command("volume", {"volume": new_volume})
    await message.answer(result.get("status", f"🔊 Громкость {new_volume}%"))

@radio_router.message(F.text == "📜 ПЛЕЙЛИСТ")
async def show_playlist(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    pl = get_valid_playlist()
    if not pl:
        await message.answer("📜 Плейлист пуст")
        return
    buttons = [[InlineKeyboardButton(text=f"{i+1}. {track['name']} ▶️", callback_data=f"play_{i}")] for i, track in enumerate(pl)]
    await message.answer(f"📜 *Плейлист* ({len(pl)} треков)\n\nНажмите на трек для воспроизведения:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

@radio_router.callback_query(F.data.startswith("play_"))
async def play_selected_track(callback: CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("⛔ Доступ запрещён")
        return
    track_index = int(callback.data.split("_")[1])
    pl = get_valid_playlist()
    if track_index >= len(pl):
        await callback.answer("❌ Трек не найден")
        return
    track = pl.pop(track_index)
    pl.insert(0, track)
    with open(PLAYLIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(pl, f, indent=2, ensure_ascii=False)
    await send_http_command("stop")
    await asyncio.sleep(1)
    await send_http_command("start")
    await callback.answer(f"🎵 {track['name']}")
    await callback.message.answer(f"✅ Сейчас играет: {track['name']}")

@radio_router.message(F.text == "🔄 ОБНОВИТЬ")
async def sync_playlist(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("🔄 Синхронизация с Google Drive...")
    import subprocess
    subprocess.run(["python3", "/home/ubuntu/radio_bot/sync_drive.py"], capture_output=True, text=True)
    pl = get_valid_playlist()
    await message.answer(f"✅ Готово! {len(pl)} треков")
