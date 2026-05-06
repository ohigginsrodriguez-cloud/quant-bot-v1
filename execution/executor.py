from datetime import datetime
from database.models.trade import Trade
import logging

class Executor:
    def __init__(self, repository):
        self.repository = repository

    def execute(self, signal, price, symbol):
        open_trade = self.repository.get_open_trade(symbol)

        if signal == "BUY":
            if open_trade:
                logging.info("Trade already open, skipping BUY")
                return
            
            logging.info("Executing BUY order")
            trade = Trade(symbol, "BUY", price, datetime.now(), "OPEN")
            self.repository.save(trade)

        elif signal == "SELL":
            if not open_trade:
                logging.info("No open trade to close")
                return
            
            logging.info("Executing SELL order")

            # Aquí luego cerraremos el trade (siguiente paso)
            # por ahora solo log
            
        else:
            logging.info("No action")