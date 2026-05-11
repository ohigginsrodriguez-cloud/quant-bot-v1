import logging
import pandas as pd
from indicators.atr import calculate_atr
from backtest.simulator import BacktestSimulator, FOREX
from backtest.metrics import calculate_metrics


class BacktestEngine:

    def __init__(self, strategy, initial_balance=10000, warmup=100, market_type=FOREX):
        self.strategy = strategy
        self.initial_balance = initial_balance
        self.warmup = warmup
        self.market_type = market_type

    def run(self, data):
        simulator = BacktestSimulator(
            initial_balance=self.initial_balance,
            market_type=self.market_type
        )

        logging.info(f"Starting backtest | Candles: {len(data)} | Warmup: {self.warmup} | Market: {self.market_type}")

        for i in range(self.warmup, len(data)):
            subset = data.iloc[:i].copy()

            if isinstance(subset['Close'], pd.DataFrame):
                subset['Close'] = subset['Close'].squeeze()

            if not isinstance(subset['Close'], pd.Series):
                continue

            try:
                result = self.strategy.generate_signal(subset)
            except Exception as e:
                logging.warning(f"Signal error at candle {i}: {e}")
                continue

            signal = result['signal']
            stop_loss = result['stop_loss']
            take_profit = result['take_profit']

            price = float(subset['Close'].iloc[-1])
            timestamp = subset.index[-1]

            try:
                atr = float(calculate_atr(subset).iloc[-1])
            except Exception:
                continue

            if not atr or atr != atr:
                continue

            simulator.step(signal, price, stop_loss, take_profit, atr, timestamp)

        metrics = calculate_metrics(simulator.closed_trades, self.initial_balance)
        return metrics, simulator.closed_trades