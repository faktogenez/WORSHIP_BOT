import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from aiogram import Bot
from bot_db import get_verse_by_date, get_schedule_settings
import logging

logger = logging.getLogger(__name__)
scheduler = AsyncIOScheduler()

async def send_bible_message(bot: Bot, channel_id: str):
    """Отправить библейское послание"""
    today = datetime.now().strftime("%Y-%m-%d")
    verse = get_verse_by_date(today)
    
    if verse:
        title, content, prayer = verse
        message = f"""📖 *{title}*

{content}

🙏 *МОЛИТВА*
{prayer}

---
_Послание на {datetime.now().strftime("%d %B %Y")} года_ ✝️"""
    else:
        message = f"""📖 *Послание на {datetime.now().strftime("%d %B %Y")} года*

Сегодняшнего послания ещё нет в базе данных.

Администратор добавит его позже. Благословенного дня! ✝️"""
    
    try:
        await bot.send_message(channel_id, message, parse_mode="Markdown")
        logger.info(f"Bible message sent to {channel_id}")
    except Exception as e:
        logger.error(f"Failed to send bible message: {e}")

def setup_bible_scheduler(bot: Bot, channel_id: str):
    """Настроить планировщик библейских посланий"""
    
    def schedule_jobs():
        # Удаляем старые задачи
        scheduler.remove_all_jobs()
        
        # Получаем настройки
        morning_hour, morning_minute, evening_hour, evening_minute, enabled = get_schedule_settings()
        
        if not enabled:
            logger.info("Bible scheduler is disabled")
            return
        
        # Утренняя рассылка
        scheduler.add_job(
            send_bible_message,
            CronTrigger(hour=morning_hour, minute=morning_minute),
            args=[bot, channel_id],
            id="morning_bible",
            replace_existing=True
        )
        
        # Вечерняя рассылка
        scheduler.add_job(
            send_bible_message,
            CronTrigger(hour=evening_hour, minute=evening_minute),
            args=[bot, channel_id],
            id="evening_bible",
            replace_existing=True
        )
        
        logger.info(f"Bible scheduler configured: {morning_hour:02d}:{morning_minute:02d} and {evening_hour:02d}:{evening_minute:02d}")
    
    schedule_jobs()
    scheduler.start()
    
    # Возвращаем функцию для обновления настроек
    return schedule_jobs