from datetime import datetime, UTC
from database.models.trade import Trade
from core.signals import BUY, SELL, HOLD
from core.positions import SHORT, LONG
import logging

class Executor:
    def __init__(self, repository, risk_manager, account):
        self.repository = repository
        self.risk_manager = risk_manager
        self.account = account

    def execute(self, signal, price, symbol, stop_loss):
        open_trade = self.repository.get_open_trade(symbol)

        # SI HAY TRADE ABIERTO
        if open_trade:
            trade_id = open_trade["id"]
            side = open_trade["side"]
            entry_price = open_trade["entry_price"]
            size = open_trade["size"]
            stop_loss_db = open_trade["stop_loss"]

            # STOP LOSS
            if side == LONG and price <= stop_loss_db:
                pnl = (price - entry_price) * size
                logging.info(f"STOP LOSS HIT (LONG) | PnL: {pnl:.3f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)
                return

            if side == SHORT and price >= stop_loss_db:
                pnl = (entry_price - price) * size
                logging.info(f"STOP LOSS HIT (SHORT) | PnL: {pnl:.3f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)
                return

            #HOLD
            if signal == HOLD:
                logging.info("Holding position")
                return

            #REVERSALS
            if side == LONG and signal == SELL:
                pnl = (price - entry_price) * size
                logging.info(f"Closing LONG | PnL: {pnl:.3f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)

                new_size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
                logging.info(f"Reversing to SHORT | Size: {new_size:.2f}")

                size = round(size, 2)
                price = round(price, 5)

                new_trade = Trade(symbol, SHORT, new_size, price, datetime.now(UTC), "OPEN", stop_loss=stop_loss)
                self.repository.save(new_trade)
                return

            if side == SHORT and signal == BUY:
                pnl = (entry_price - price) * size
                logging.info(f"Closing SHORT | PnL: {pnl:.3f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)

                new_size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
                logging.info(f"Reversing to LONG | Size: {new_size:.2f}")

                size = round(size, 2)
                price = round(price, 5)

                new_trade = Trade(symbol, LONG, new_size, price, datetime.now(UTC), "OPEN", stop_loss=stop_loss)
                self.repository.save(new_trade)
                return

            #MISMA DIRECCIÓN
            logging.info(f"Already in {side}, skipping")
            return

        #NO HAY TRADE ABIERTO
        if signal == HOLD:
            logging.info("No action")
            return

        if stop_loss is None:
            logging.warning("Stop loss is None, skipping trade")
            return

        size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)

        if signal == BUY:
            logging.info(f"Opening LONG | Size: {size:.2f}")
            trade = Trade(symbol, LONG, size, price, datetime.now(UTC), "OPEN", stop_loss=stop_loss)

            size = round(size, 2)
            price = round(price, 5)
            
            self.repository.save(trade)

        elif signal == SELL:
            logging.info(f"Opening SHORT | Size: {size:.2f}")
            trade = Trade(symbol, SHORT, size, price, datetime.now(UTC), "OPEN", stop_loss=stop_loss)

            size = round(size, 2)
            price = round(price, 5)

            self.repository.save(trade)