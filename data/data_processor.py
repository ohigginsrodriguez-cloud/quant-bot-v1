import pandas as pd


def process_data(df):
    df = df.copy()


    df['return'] = df['Close'].pct_change()
    df['volatility'] = df['Return'].rolling(window=30).std()

    df = df.dropna()
    
    return df