from indicators.volatility import calculate_volatility
from strategies.base_strategy import BaseStrategy
from core.signals import BUY, HOLD

class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df):

        if df is None or df.empty:
            return HOLD

        window = self.params['window']
        threshold = self.params['threshold']

        volatility = calculate_volatility(df['Close'], window)
        last_vol = volatility.iloc[-1]
        price = df['Close'].iloc[-1]

        if last_vol > threshold:
            stop_loss = price - 0.002  # ~20 pips (LONG)
            return {
                "signal": BUY,
                "stop_loss":  stop_loss
            }

        return {"signal": HOLD, "stop_loss": None} 