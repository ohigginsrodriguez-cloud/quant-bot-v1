import pandas as pd

def calculate_bollinger(closes, window=20, std=2):

    sma = closes.rolling(window).mean()
    rolling_std = closes.rolling(window).std()

    upper_band = sma + (std * rolling_std)
    lower_band = sma - (std * rolling_std)

    return lower_band, upper_band