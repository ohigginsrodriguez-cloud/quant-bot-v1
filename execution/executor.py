from datetime import datetime, UTC
from database.models.trade import Trade
from core.signals import BUY, SELL, HOLD
from core.positions import SHORT, LONG
import logging

class Executor:
    def __init__(self, repository, risk_manager, account, exit_manager):
        self.repository = repository
        self.risk_manager = risk_manager
        self.account = account
        self.exit_manager = exit_manager

    def _calculate_pnl(self, side, entry, exit_price, size):
        return self.exit_manager._calculate_pnl(side, entry, exit_price, size)

    def execute(self, signal, price, symbol, stop_loss, take_profit, atr):
        open_trade = self.repository.get_open_trade(symbol)

        # SI HAY TRADE ABIERTO
        if open_trade:
            open_trade = dict(open_trade)
            trade_id = open_trade["id"]
            side = open_trade["side"]
            entry_price = open_trade["entry_price"]
            size = open_trade["size"]

            new_sl = self.exit_manager.update_trailing_stop(open_trade, price, atr)

            #SOLO ACTUALIZA SI CAMBIO
            if new_sl !=open_trade['stop_loss']:
                logging.info(f"Updating trailing SL: {open_trade['stop_loss']} -> {new_sl}")
                self.repository.update_stop_loss(trade_id, new_sl)
                #ACTUALIZAR TAMBIEN EN MEMORIA
                open_trade['stop_loss'] = new_sl

            exit_type, pnl = self.exit_manager.check_exit(open_trade, price)

            #SL Y TP
            if exit_type:
                logging.info(f"{exit_type} HIT | PnL: {pnl:.2f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)
                return

            #HOLD
            if signal == HOLD:
                logging.info("Holding position")
                return

            #REVERSALS
            if side == LONG and signal == SELL:
                pnl = self._calculate_pnl(LONG, entry_price, price, size)
                logging.info(f"Closing LONG | PnL: {pnl:.2f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)

                new_size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
                logging.info(f"Reversing to SHORT | Size: {new_size:.2f} lots")
                new_trade = Trade(symbol, SHORT, new_size, round(price, 5), datetime.now(UTC), "OPEN", stop_loss=stop_loss, take_profit=take_profit)
                self.repository.save(new_trade)
                return

            if side == SHORT and signal == BUY:
                pnl = self._calculate_pnl(SHORT, entry_price, price, size)
                logging.info(f"Closing SHORT | PnL: {pnl:.2f}")
                self.repository.close_trade(trade_id, price, pnl)
                self.account.update_balance(pnl)

                new_size = self.risk_manager.calculate_position_size(self.account.balance, price, stop_loss)
                logging.info(f"Reversing to LONG | Size: {new_size:.2f} lots")

                new_trade = Trade(symbol, LONG, new_size, round(price, 5), datetime.now(UTC), "OPEN", stop_loss=stop_loss, take_profit=take_profit)
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
            logging.info(f"Opening LONG | Size: {size:.2f} lots")
            trade = Trade(symbol, LONG, round(size, 2),round (price, 5), datetime.now(UTC), "OPEN", stop_loss=stop_loss, take_profit=take_profit)
            self.repository.save(trade)

        elif signal == SELL:
            logging.info(f"Opening SHORT | Size: {size:.2f}")
            trade = Trade(symbol, SHORT, round(size, 2), round(price, 5), datetime.now(UTC), "OPEN", stop_loss=stop_loss, take_profit=take_profit)
            self.repository.save(trade)