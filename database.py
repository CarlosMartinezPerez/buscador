import sqlite3
import datetime
from config import Config

def get_connection():
    return sqlite3.connect(Config.DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS editais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT,
                topics TEXT,
                stipend TEXT,
                deadline TEXT,
                summary TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def is_url_seen(url: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM editais WHERE url = ?", (url,))
        return cursor.fetchone() is not None

def save_edital(url: str, title: str, topics: str, stipend: str, deadline: str, summary: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO editais (url, title, topics, stipend, deadline, summary, found_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (url, title, topics, stipend, deadline, summary, datetime.datetime.now().isoformat()))
        conn.commit()

def get_all_saved_urls():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM editais")
        return {row[0] for row in cursor.fetchall()}
