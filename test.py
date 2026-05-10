print('1. Проверка импорта py_tgcalls...')
from py_tgcalls import GroupCallFactory
print('    GroupCallFactory найден')

print('2. Проверка типов...')
from py_tgcalls.types import AudioQuality
print('    AudioQuality найден')

print('3. Проверка Telethon...')
from telethon import TelegramClient
print('    Telethon найден')

print()
print(' Все импорты успешны!')
