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

        if signal == HOLD:
            logging.info("No action")
            return
        
        if open_trade is None:
            size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
            if signal == BUY:
                logging.info(f"Opening LONG | Size: {size:.2f}")
                trade = Trade(symbol=symbol, side=LONG, size=size, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN", stop_loss=stop_loss)
                self.repository.save(trade)

            elif signal == SELL:
                stop_loss_price = price * 1.01
                size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
                logging.info(f"Opening SHORT | Size: {size:.2f}")
                trade = Trade(symbol=symbol, side=SHORT, size=size, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN", stop_loss=stop_loss)
                self.repository.save(trade)

            return
        
        # si ya hay posicion abierta, decidir cerrar/revertir
        trade_id = open_trade["id"]
        side = open_trade["side"]
        entry_price = open_trade["entry_price"]
        size = open_trade['size']

        if side == LONG and signal == SELL:
            size = open_trade['size']
            pnl = (price - entry_price) * size
            logging.info(f"Closing LONG with PnL: {pnl:.3f}")
            self.repository.close_trade(trade_id, price, pnl)
            self.account.update_balance(pnl)

            # abrir short inmediatamente
            size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
            logging.info(f"Reversing to SHORT | size: {size:.2f}")
            new_trade = Trade(symbol=symbol, side=SHORT, size=size, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN", stop_loss=stop_loss)
            self.repository.save(new_trade)

        elif side == SHORT and signal == BUY:
            size = open_trade['size']
            pnl = (entry_price - price) * size
            logging.info(f"Closing SHORT with PnL: {pnl:.3f}")
            self.repository.close_trade(trade_id, price, pnl)
            self.account.update_balance(pnl)

            # abrir long inmediatamente
            size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
            logging.info(f"Reversing to LONG | Size: {size:.2f}")
            new_trade = Trade(symbol=symbol, side=LONG, size=size, entry_price=price, entry_timestamp=datetime.now(UTC), status="OPEN", stop_loss=stop_loss)
            self.repository.save(new_trade)

        elif side == LONG and signal == BUY:
            logging.info("Already in LONG, skipping")

        elif side == SHORT and signal == SELL:
            logging.info("Already in Short, skipping")