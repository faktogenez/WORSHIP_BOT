import asyncio
import subprocess
import sys
import os

async def run_bot():
    """Запуск main.py"""
    proc = await asyncio.create_subprocess_exec(
        sys.executable, 'main.py',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    async for line in proc.stdout:
        print(f'[BOT] {line.decode().strip()}')
    
    await proc.wait()

async def run_userbot():
    """Запуск radio_userbot.py"""
    proc = await asyncio.create_subprocess_exec(
        sys.executable, 'radio_userbot.py',
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    async for line in proc.stdout:
        print(f'[USERBOT] {line.decode().strip()}')
    
    await proc.wait()

async def main():
    print("="*50)
    print("🚀 ЗАПУСК БОТА И USERBOT")
    print("="*50)
    
    # Запускаем оба процесса параллельно
    await asyncio.gather(
        run_bot(),
        run_userbot()
    )

if __name__ == "__main__":
    asyncio.run(main())
