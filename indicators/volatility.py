import pandas as pd

def calculate_volatility(close_prices, window):
    # asegurar que sea Serie y no escalar
    if not isinstance(close_prices, pd.Series):
        raise ValueError(f"close_prices debe ser pd.Series, recibió {type(close_prices)}")
    
    returns = close_prices.pct_change()
    volatility = returns.rolling(window=window).std()

    return volatility