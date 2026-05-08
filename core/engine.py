import logging

class TradingEngine:

    def __init__(self, strategy, risk_manager, executor, repository):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.executor = executor
        self.repository = repository

    def run(self, data, symbol):
        result = self.strategy.generate_signal(data)

        signal = result['signal']
        stop_loss = result['stop_loss']
        take_profit = result['take_profit']
        
        price = data['Close'].iloc[-1]

        open_trade = self.repository.get_open_trade(symbol)

        if open_trade is None:
            open_trades = self.repository.get_open_trades()

            if not self.risk_manager.can_open_positions(open_trades):
                logging.info("Max positions reached, skipping trade")
                return signal
            
        self.executor.execute(signal, price, symbol, stop_loss, take_profit)

        return signal