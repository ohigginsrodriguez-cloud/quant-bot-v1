import logging
import pandas as pd
from indicators.atr import calculate_atr
from indicators.bollinger_bands import calculate_bollinger
from indicators.volatility import calculate_volatility
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

        # PRECALCULAR indicadores una sola vez sobre todo el dataset
        data = data.copy()
        data['ATR'] = calculate_atr(data)
        data['VOL'] = calculate_volatility(data['Close'], window=30)
        data['BB_LOWER'], data['BB_UPPER'] = calculate_bollinger(data['Close'])

        logging.info(f"Starting backtest | Candles: {len(data)} | Warmup: {self.warmup} | Market: {self.market_type}")

        for i in range(self.warmup, len(data)):
            subset = data.iloc[:i]

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

            candle = data.iloc[i - 1]
            price = float(candle['Close'])
            high = float(candle['High'])
            low = float(candle['Low'])
            atr = float(candle['ATR'])
            timestamp = data.index[i - 1]

            if pd.isna(atr):
                continue

            logging.debug(f"{timestamp} | {signal} | price: {price:.5f} | SL: {stop_loss} | TP: {take_profit}")

            simulator.step(signal, price, high, low, stop_loss, take_profit, atr, timestamp)

        metrics = calculate_metrics(simulator.closed_trades, self.initial_balance)
        return metrics, simulator.closed_trades, simulator.equity_curve