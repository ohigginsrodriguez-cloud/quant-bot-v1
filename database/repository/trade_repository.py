from database.db import get_connection
import logging

class TradeRepository:

    def save(self, trade):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trades (symbol, action, price, timestamp, status)
            VALUES (?, ?, ?, ?, ?)
            """, (trade.symbol, trade.action, trade.price, str(trade.timestamp), trade.status)
        )
        conn.commit()
        conn.close()
        logging.info(f"Saving trade: {trade.action} {trade.symbol}")


    def get_open_trade(self, symbol):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM trades
            WHERE symbol = ? AND status = 'OPEN'
            ORDER BY id DESC
            LIMIT 1
            """, (symbol,)
        )

        row = cursor.fetchone()
        conn.close()

        return row # None si no hay
    
    def get_open_trades(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM trades
            WHERE status = 'OPEN'
            """
        )

        rows = cursor.fetchall()
        conn.close()

        return rows