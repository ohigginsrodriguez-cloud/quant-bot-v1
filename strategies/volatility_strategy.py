import pandas as pd
from strategies.base_strategy import BaseStrategy

class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df):
        if df is None or df.empty:
            return None

        last_vol = df['volatility'].iloc[-1]
        threshold = self.params['threshold']

        if last_vol > threshold:
            return "BUY"

        return "HOLD"