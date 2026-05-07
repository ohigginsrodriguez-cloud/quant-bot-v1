import pandas as pd

def calculate_volatility(close_prices, window):
    returns = close_prices.pct_change()
    volatility = returns.rolling(window=window).std()

    return volatility