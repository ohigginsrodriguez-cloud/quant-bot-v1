import sqlite3
from pathlib import Path
from config.settings import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        action TEXT,
        price REAL,
        timestamp TEXT,
        status TEXT)
        """
    )

    conn.commit()
    conn.close()