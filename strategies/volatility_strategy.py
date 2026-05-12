from strategies.base_strategy import BaseStrategy
from core.signals import BUY, SELL, HOLD
import pandas as pd


class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df, idx):

        if df is None or df.empty:
            return {
                "signal": HOLD, 
                "stop_loss": None, 
                "take_profit": None}

        required = ['ATR', 'VOL', 'BB_LOWER', 'BB_UPPER']
        if not all(col in df.columns for col in required):
            raise ValueError("Indicators not found in dataframe")

        threshold = self.params['threshold']

        vol = df['VOL'].iloc[idx]
        last_close = df['Close'].iloc[idx]
        last_lower = df['BB_LOWER'].iloc[idx]
        last_upper = df['BB_UPPER'].iloc[idx]
        atr = df['ATR'].iloc[idx]

        if any(pd.isna(x) for x in [vol, last_close, last_lower, last_upper, atr]):
            return {
                "signal": HOLD, 
                "stop_loss": None, 
                "take_profit": None}

        if vol > threshold and last_close <= last_lower:
            return {
                "signal": BUY,
                "stop_loss": last_close - (atr * 1.5),
                "take_profit": last_close + (atr * 3)
            }

        if vol > threshold and last_close >= last_upper:
            return {
                "signal": SELL,
                "stop_loss": last_close + (atr * 1.5),
                "take_profit": last_close - (atr * 3)
            }

        return {
            "signal": HOLD, 
            "stop_loss": None, 
            "take_profit": None}