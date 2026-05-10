import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)

RADIO_API_URL = "http://localhost:8765"
http_session = None

async def get_http_session():
    global http_session
    if http_session is None or http_session.closed:
        timeout = aiohttp.ClientTimeout(total=10, connect=5)
        http_session = aiohttp.ClientSession(timeout=timeout)
    return http_session

async def radio_health_check():
    try:
        session = await get_http_session()
        async with session.get(f"{RADIO_API_URL}/health") as resp:
            return resp.status == 200
    except:
        return False

async def send_http_command(endpoint: str, data: dict = None):
    if not await radio_health_check():
        return {"status": "🔌 Радио-сервис не отвечает"}
    
    try:
        session = await get_http_session()
        if endpoint == "status":
            async with session.get(f"{RADIO_API_URL}/{endpoint}") as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"is_playing": False, "current_volume": 100}
        else:
            async with session.post(f"{RADIO_API_URL}/{endpoint}", json=data or {}) as resp:
                if resp.status == 200:
                    return await resp.json()
                return {"status": f"❌ Ошибка {resp.status}"}
    except Exception as e:
        return {"status": f"❌ Ошибка"}

async def get_radio_status():
    data = await send_http_command("status")
    return data.get("is_playing", False), data.get("current_volume", 100)
