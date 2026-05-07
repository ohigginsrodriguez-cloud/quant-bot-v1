from datetime import datetime, UTC
from database.models.trade import Trade
from core.signals import BUY, SELL, HOLD
from core.positions import SHORT, LONG
import logging

class Executor:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, signal, price, symbol):
        open_trade = self.repository.get_open_trade(symbol)

        if signal == HOLD:
            logging.info("No action")
            return
        
        if open_trade is None:
            if signal == BUY:
                logging.info("Opening LONG")
                trade = Trade(symbol=symbol, side=LONG, size=1, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN")
                self.repository.save(trade)

            elif signal == SELL:
                logging.info("Opening SHORT")
                trade = Trade(symbol=symbol, side=SHORT, size=1, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN")
                self.repository.save(trade)

            return
        
        # si ya hay posicion abierta, decidir cerrar/revertir
        trade_id = open_trade["id"]
        side = open_trade["side"]
        entry_price = open_trade["entry_price"]
        size = open_trade['size']

        if side == LONG and signal == SELL:
            pnl = (price - entry_price) * size
            logging.info(f"Closing LONG with PnL: {pnl:.3f}")
            self.repository.close_trade(trade_id, price, pnl)

            # abrir short inmediatamente
            logging.info("Reversing to SHORT")
            new_trade = Trade(symbol=symbol, side=SHORT, size=1, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN")
            self.repository.save(new_trade)

        elif side == SHORT and signal == BUY:
            pnl = (entry_price - price) * size
            logging.info(f"Closing SHORT with PnL: {pnl:.3f}")
            self.repository.close_trade(trade_id, price, pnl)

            # abrir long inmediatamente
            logging.info("Reversing to LONG")
            new_trade = Trade(symbol=symbol, side=LONG, size=1, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN")
            self.repository.save(new_trade)

        elif side == LONG and signal == BUY:
            logging.info("Already in LONG, skipping")

        elif side == SHORT and signal == SELL:
            logging.info("Already in Short, skipping")