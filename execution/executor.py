import logging

class Executor:

    def execute(self, signal):
        if signal == "BUY":
            logging.info("Exexuting BUY order")
        elif signal == "SELL":
            logging.info("Executing SELL order")
        else:
            logging.info("No action")