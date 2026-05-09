from indicators.volatility import calculate_volatility
from strategies.base_strategy import BaseStrategy
from core.signals import BUY, HOLD

class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df):

        if df is None or df.empty:
            return {
                "signal": HOLD,
                "stop_loss": None,
                "take_profit": None
            }

        window = self.params['window']
        threshold = self.params['threshold']

        volatility = calculate_volatility(df['Close'], window)

        price = df['Close'].iloc[-1]
        vol = volatility.iloc[-1]

        if vol > threshold:

            stop_loss = price - vol
            take_profit = price + (vol * 2)

            return {
                "signal": BUY,
                "stop_loss":  stop_loss,
                "take_profit": take_profit
            }

        return {
            "signal": HOLD, 
            "stop_loss": None,
            "take_profit": None} 