#!/usr/bin/env python3
import asyncio
import sys
import json
import signal
from pathlib import Path
from aiohttp import web

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream
from config import API_ID, API_HASH, DEFAULT_CHANNEL

PLAYLIST_FILE = Path(__file__).parent / "playlist.json"
STATUS_FILE = Path(__file__).parent / "radio_status.json"

app = None
calls = None
is_playing = False
current_volume = 100
current_track_index = 0
playlist = []
http_runner = None

def load_playlist():
    global playlist, current_track_index
    try:
        if PLAYLIST_FILE.exists():
            with open(PLAYLIST_FILE, 'r') as f:
                playlist = json.load(f)
            if playlist and current_track_index >= len(playlist):
                current_track_index = 0
        else:
            playlist = []
        print(f"📜 Плейлист: {len(playlist)} треков")
    except Exception as e:
        print(f"Ошибка загрузки: {e}")

def save_status():
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump({
                "is_playing": is_playing,
                "current_volume": current_volume,
                "current_track_index": current_track_index,
                "current_track": playlist[current_track_index]["name"] if playlist else None
            }, f)
    except Exception as e:
        print(f"Ошибка статуса: {e}")

def load_status():
    global current_volume, current_track_index
    try:
        if STATUS_FILE.exists():
            with open(STATUS_FILE, 'r') as f:
                data = json.load(f)
                current_volume = data.get("current_volume", 100)
                current_track_index = data.get("current_track_index", 0)
    except Exception as e:
        print(f"Ошибка статуса: {e}")

async def stop_playback():
    global calls, app, is_playing
    try:
        if calls:
            await calls.leave_call(DEFAULT_CHANNEL)
            await calls.stop()
            calls = None
    except Exception as e:
        print(f"Ошибка: {e}")
    try:
        if app:
            await app.stop()
            app = None
    except Exception as e:
        print(f"Ошибка: {e}")
    is_playing = False
    save_status()

async def start_playback():
    global app, calls, is_playing, playlist, current_track_index, current_volume
    
    load_playlist()
    
    if not playlist:
        return "❌ Плейлист пуст"
    
    if current_track_index >= len(playlist):
        current_track_index = 0
    
    track = playlist[current_track_index]
    track_path = track["path"]
    
    if not Path(track_path).exists():
        return f"❌ Файл не найден: {track['name']}"
    
    await stop_playback()
    await asyncio.sleep(1)
    
    try:
        app = Client("radio_session", api_id=API_ID, api_hash=API_HASH)
        calls = PyTgCalls(app)
        
        await app.start()
        await calls.start()
        await calls.play(DEFAULT_CHANNEL, MediaStream(str(track_path)))
        await calls.change_volume_call(DEFAULT_CHANNEL, volume=current_volume)
        
        is_playing = True
        save_status()
        return f"✅ Сейчас играет: {track['name']}"
    except Exception as e:
        print(f"Ошибка: {e}")
        return f"❌ Ошибка: {str(e)[:100]}"

async def cmd_start():
    if is_playing:
        return "✅ Хвала уже играет"
    return await start_playback()

async def cmd_stop():
    if not is_playing:
        return "⏹️ Хвала уже остановлена"
    await stop_playback()
    return "⏹️ Хвала остановлена"

async def cmd_volume(percent):
    global current_volume, calls
    current_volume = max(0, min(200, percent))
    save_status()
    if calls and is_playing:
        try:
            await calls.change_volume_call(DEFAULT_CHANNEL, volume=current_volume)
        except Exception as e:
            print(f"Ошибка: {e}")
    return f"🔊 Громкость {current_volume}%"

def cmd_status():
    return {
        "is_playing": is_playing,
        "current_volume": current_volume,
        "current_track": playlist[current_track_index]["name"] if playlist else None,
        "total_tracks": len(playlist)
    }

async def handle_start(request):
    result = await cmd_start()
    return web.json_response({"status": result})

async def handle_stop(request):
    result = await cmd_stop()
    return web.json_response({"status": result})

async def handle_volume(request):
    try:
        data = await request.json()
        volume = data.get("volume", 100)
        result = await cmd_volume(volume)
        return web.json_response({"status": result})
    except:
        return web.json_response({"status": "❌ Неверный формат"}, status=400)

async def handle_status(request):
    return web.json_response(cmd_status())

async def handle_health(request):
    return web.json_response({"status": "ok", "playing": is_playing})

async def start_http_server():
    app_web = web.Application()
    app_web.router.add_post("/start", handle_start)
    app_web.router.add_post("/stop", handle_stop)
    app_web.router.add_post("/volume", handle_volume)
    app_web.router.add_get("/status", handle_status)
    app_web.router.add_get("/health", handle_health)
    
    runner = web.AppRunner(app_web)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8765)
    await site.start()
    print("✅ HTTP сервер запущен")
    return runner

async def shutdown():
    print("\n⏹️ Завершение...")
    await stop_playback()
    if http_runner:
        await http_runner.cleanup()
    print("✅ Завершено")

async def main():
    global http_runner
    load_playlist()
    load_status()
    
    print("="*50)
    print("🔊 ХВАЛЫ")
    print("="*50)
    print(f"Статус: {'Играет' if is_playing else 'Остановлено'}")
    print(f"Громкость: {current_volume}%")
    print(f"Треков: {len(playlist)}")
    if playlist and current_track_index < len(playlist):
        print(f"Текущий: {playlist[current_track_index]['name']}")
    print("="*50)
    
    http_runner = await start_http_server()
    print("\n✅ Готов. Ожидание команд...\n")
    
    loop = asyncio.get_running_loop()
    for sig in [signal.SIGTERM, signal.SIGINT]:
        loop.add_signal_handler(sig, lambda: asyncio.create_task(shutdown()))
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ Остановка")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
