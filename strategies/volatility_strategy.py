from strategies.base_strategy import BaseStrategy
from core.signals import BUY, SELL, HOLD


class VolatilityStrategy(BaseStrategy):

    def generate_signal(self, df):

        if df is None or df.empty:
            return {"signal": HOLD, "stop_loss": None, "take_profit": None}

        required = ['ATR', 'VOL', 'BB_LOWER', 'BB_UPPER']
        if not all(col in df.columns for col in required):
            # fallback: calcular si no vienen precalculados (modo live)
            from indicators.volatility import calculate_volatility
            from indicators.bollinger_bands import calculate_bollinger
            from indicators.atr import calculate_atr

            df = df.copy()
            df['ATR'] = calculate_atr(df)
            df['VOL'] = calculate_volatility(df['Close'], window=self.params['window'])
            df['BB_LOWER'], df['BB_UPPER'] = calculate_bollinger(df['Close'])

        threshold = self.params['threshold']

        vol = df['VOL'].iloc[-1]
        last_close = df['Close'].iloc[-1]
        last_lower = df['BB_LOWER'].iloc[-1]
        last_upper = df['BB_UPPER'].iloc[-1]
        atr = df['ATR'].iloc[-1]

        import pandas as pd
        if any(pd.isna(x) for x in [vol, last_close, last_lower, last_upper, atr]):
            return {"signal": HOLD, "stop_loss": None, "take_profit": None}

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

        return {"signal": HOLD, "stop_loss": None, "take_profit": None}