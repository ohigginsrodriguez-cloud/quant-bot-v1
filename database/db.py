import sqlite3
from pathlib import Path
from config.settings import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        side TEXT NOT NULL,
        size REAL NOT NULL,
        entry_price REAL NOT NULL,
        entry_timestamp TEXT NOT NULL,
        status TEXT NOT NULL,
        exit_price REAL,
        exit_timestamp TEXT,
        pnl REAL,
        stop_loss REAL,
        take_profit REAL
        )
        """
    )

    conn.commit()
    conn.close()