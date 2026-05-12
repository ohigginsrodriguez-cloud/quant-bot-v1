from indicators.atr import calculate_atr
from utils.validators import validate_signal
from indicators.volatility import calculate_volatility
from indicators.bollinger_bands import calculate_bollinger
import logging

class TradingEngine:

    def __init__(self, strategy, risk_manager, executor, repository):
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.executor = executor
        self.repository = repository

    def run(self, data, symbol):

        if len(data) < 3:
            logging.warning("Not enogh data")
            return None

        data = data.copy()
        data['ATR'] = calculate_atr(data)
        data['VOL'] = calculate_volatility(data['Close'], window=self.strategy.params['window'])
        data['BB_LOWER'], data['BB_UPPER'] = calculate_bollinger(data['Close'])

        idx = -2
        result = self.strategy.generate_signal(data, idx)

        if not validate_signal(result):
            logging.error("Strategy returned invalid signal format")
            return None

        signal = result['signal']
        stop_loss = result['stop_loss']
        take_profit = result['take_profit']
        
        price = data['Close'].iloc[idx]
        atr = data['ATR'].iloc[idx]

        logging.info(f"ATR: {atr:.5f} ({atr / 0.0001:.1f} pips)")

        open_trade = self.repository.get_open_trade(symbol)

        if open_trade is None:
            open_trades = self.repository.get_open_trades()

            if not self.risk_manager.can_open_positions(open_trades):
                logging.info("Max positions reached, skipping trade")
                return signal
            
        self.executor.execute(signal, price, symbol, stop_loss, take_profit, atr)

        return signal