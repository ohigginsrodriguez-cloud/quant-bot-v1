from indicators.volatility import calculate_volatility
from indicators.bollinger_bands import calculate_bollinger
from indicators.atr import calculate_atr
from strategies.base_strategy import BaseStrategy
from core.signals import BUY, SELL, HOLD

class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df):

        if df is None or df.empty:
            return {
                "signal": HOLD,
                "stop_loss": None,
                "take_profit": None
            }
        
        threshold = self.params['threshold']
        window = self.params['window']

        volatility = calculate_volatility(df['Close'], window)
        vol = volatility.iloc[-1]

        lower_band, upper_band = calculate_bollinger(df['Close'])
        
        last_close = df['Close'].iloc[-1]
        last_lower = lower_band.iloc[-1]
        last_upper = upper_band.iloc[-1]

        atr = calculate_atr(df).iloc[-1]

        if vol > threshold and last_close <= last_lower:

            sl = last_close - (atr * 1.5)
            tp = last_close + (atr * 3)

            return{
                "signal": BUY,
                "stop_loss": sl,
                "take_profit": tp
            }
        
        if vol > threshold and last_close >= last_upper:

            sl = last_close + (atr * 1.5)
            tp = last_close - (atr * 3)

            return{
                "signal": SELL,
                "stop_loss": sl,
                "take_profit": tp
            }
        
        return{
            "signal": HOLD,
            "stop_loss": None,
            "take_profit": None
        }