from database.db import get_connection
import logging

class TradeRepository:

    def save(self, trade):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO trades (symbol, side, size, entry_price, entry_timestamp, status, exit_price, exit_timestamp, pnl, stop_loss, take_profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (trade.symbol,
                  trade.side,
                  trade.size,
                  trade.entry_price,
                  trade.entry_timestamp.isoformat(),
                  trade.status,
                  trade.exit_price,
                  trade.exit_timestamp.isoformat() if trade.exit_timestamp else None,
                  trade.pnl,
                  trade.stop_loss,
                  trade.take_profit
                  )
        )

        conn.commit()
        conn.close()
        logging.info(f"Saving trade: {trade.side} {trade.symbol}")


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
    
    def close_trade(self, trade_id, exit_price, pnl):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE trades
            SET status = 'CLOSED',
            exit_price = ?,
            exit_timestamp = CURRENT_TIMESTAMP,
            pnl = ?
            WHERE id = ?
            """, (exit_price, pnl, trade_id)
        )

        conn.commit()
        conn.close()

    def update_stop_loss(self, trade_id, new_sl):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE trades
            SET stop_loss = ?
            WHERE id = ?
            """, (new_sl, trade_id)
        )

        conn.commit()
        conn.close()