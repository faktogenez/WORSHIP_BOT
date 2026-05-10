import sqlite3
from datetime import datetime
from pathlib import Path

# Путь к базе данных
DB_PATH = Path(__file__).parent / "verses.db"

def init_db():
    """Инициализация базы данных"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Таблица стихов/посланий
        c.execute('''
            CREATE TABLE IF NOT EXISTS bible_verses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                title TEXT,
                content TEXT,
                prayer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица статистики
        c.execute('''
            CREATE TABLE IF NOT EXISTS stats (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица настроек расписания
        c.execute('''
            CREATE TABLE IF NOT EXISTS schedule_settings (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                morning_hour INTEGER DEFAULT 8,
                morning_minute INTEGER DEFAULT 0,
                evening_hour INTEGER DEFAULT 20,
                evening_minute INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1
            )
        ''')
        
        # Вставляем настройки по умолчанию (если ещё нет)
        c.execute('SELECT COUNT(*) FROM schedule_settings')
        count = c.fetchone()[0]
        if count == 0:
            c.execute('''
                INSERT INTO schedule_settings (id, morning_hour, morning_minute, evening_hour, evening_minute, enabled)
                VALUES (1, 8, 0, 20, 0, 1)
            ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def save_verse(date: str, title: str, content: str, prayer: str):
    """Сохранить послание на определённую дату"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO bible_verses (date, title, content, prayer)
            VALUES (?, ?, ?, ?)
        ''', (date, title, content, prayer))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error saving verse: {e}")
        return False

def get_verse_by_date(date: str):
    """Получить послание по дате"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT title, content, prayer FROM bible_verses WHERE date = ?', (date,))
        result = c.fetchone()
        conn.close()
        return result
    except Exception as e:
        print(f"❌ Error getting verse: {e}")
        return None

def get_all_verses(limit=100):
    """Получить все послания"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT date, title, content, prayer FROM bible_verses ORDER BY date DESC LIMIT ?', (limit,))
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"❌ Error getting all verses: {e}")
        return []

def delete_verse(date: str):
    """Удалить послание по дате"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM bible_verses WHERE date = ?', (date,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error deleting verse: {e}")
        return False

def update_stats(key: str, value: str):
    """Обновить статистику"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT OR REPLACE INTO stats (key, value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (key, value))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error updating stats: {e}")
        return False

def get_stats(key: str):
    """Получить статистику по ключу"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT value FROM stats WHERE key = ?', (key,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return None

def get_schedule_settings():
    """Получить настройки расписания"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Проверяем существование таблицы
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='schedule_settings'")
        if not c.fetchone():
            conn.close()
            # Возвращаем значения по умолчанию
            return (8, 0, 20, 0, 1)
        
        c.execute('SELECT morning_hour, morning_minute, evening_hour, evening_minute, enabled FROM schedule_settings WHERE id = 1')
        result = c.fetchone()
        conn.close()
        
        if result:
            return result
        else:
            return (8, 0, 20, 0, 1)
    except Exception as e:
        print(f"❌ Error getting schedule settings: {e}")
        return (8, 0, 20, 0, 1)

def update_schedule_settings(morning_hour: int, morning_minute: int, evening_hour: int, evening_minute: int, enabled: int):
    """Обновить настройки расписания"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            UPDATE schedule_settings 
            SET morning_hour = ?, morning_minute = ?, evening_hour = ?, evening_minute = ?, enabled = ?
            WHERE id = 1
        ''', (morning_hour, morning_minute, evening_hour, evening_minute, enabled))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error updating schedule settings: {e}")
        return False

def get_verse_count():
    """Получить количество посланий в базе"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM bible_verses')
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"❌ Error getting verse count: {e}")
        return 0

def search_verses(keyword: str):
    """Поиск посланий по ключевому слову"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT date, title, content, prayer 
            FROM bible_verses 
            WHERE title LIKE ? OR content LIKE ? 
            ORDER BY date DESC 
            LIMIT 20
        ''', (f'%{keyword}%', f'%{keyword}%'))
        results = c.fetchall()
        conn.close()
        return results
    except Exception as e:
        print(f"❌ Error searching verses: {e}")
        return []

# Функция для проверки подключения к БД
def test_connection():
    """Тест подключения к базе данных"""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT sqlite_version()')
        version = c.fetchone()[0]
        conn.close()
        print(f"✅ Database connected successfully (SQLite version: {version})")
        return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

# Функция для резервного копирования БД
def backup_database():
    """Создать резервную копию базы данных"""
    try:
        import shutil
        from datetime import datetime
        
        backup_path = Path(__file__).parent / f"verses_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        shutil.copy2(DB_PATH, backup_path)
        print(f"✅ Database backed up to {backup_path}")
        return str(backup_path)
    except Exception as e:
        print(f"❌ Backup error: {e}")
        return None