#!/bin/bash
echo "🧹 НАЧАЛО ОЧИСТКИ ПРОЕКТА"
echo "========================="

# 1. Деактивируем venv если активен
deactivate 2>/dev/null

# 2. Останавливаем все процессы Python
pkill -f "python.*main.py" 2>/dev/null
pkill -f "python.*radio" 2>/dev/null
pkill -f "python.*test" 2>/dev/null
pkill -f "python.*play" 2>/dev/null

# 3. Удаляем старую виртуальную среду
echo "🗑️ Удаление venv..."
rm -rf venv

# 4. Удаляем все сессионные файлы
echo "🗑️ Удаление сессионных файлов..."
rm -f *.session *.session-journal

# 5. Удаляем временные и тестовые файлы
echo "🗑️ Удаление тестовых файлов..."
rm -f test_*.py debug_*.py play_*.py
rm -f radio_youtube.py radio_userbot.py radio_tgcaller.py

# 6. Удаляем RAW файлы (конвертированное аудио)
echo "🗑️ Удаление RAW файлов..."
rm -f music/*.raw

# 7. Очищаем кэш Python
echo "🗑️ Очистка кэша..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 8. Очищаем кэш pip
pip cache purge 2>/dev/null

echo "========================="
echo "✅ ОЧИСТКА ЗАВЕРШЕНА"
echo ""
echo "Остались только нужные файлы:"
ls -la
echo ""
echo "Теперь выполните:"
echo "python3 -m venv venv"
echo "source venv/bin/activate"
echo "pip install --upgrade pip"
echo "pip install pyrogram pytgcalls tgcalls yt-dlp"
