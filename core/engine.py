import logging

class TradingEngine:

    def __init__(self, strategy, executor, repository):
        self.strategy = strategy
        self.executor = executor
        self.repository = repository

    def run(self, data, symbol):
        signal = self.strategy.generate_signal(data)

        if signal is None:
            return None
        
        price = data['Close'].iloc[-1]

        open_trades = self.repository.get_open_trades()
        max_positions = 3 #ejemplo

        if signal == "BUY" and len(open_trades) >= max_positions:
            logging.info("Max positions reached, skipping trade")
            return signal

        self.executor.execute(signal, price, symbol)
        
        return signal