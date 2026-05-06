import pandas as pd

def process_data(df, params):
    df = df.copy()
    window = params['window']

    df['return'] = df['Close'].pct_change()
    df['volatility'] = df['return'].rolling(window=window).std()

    df = df.dropna(subset=['return', 'volatility'])
    
    return df