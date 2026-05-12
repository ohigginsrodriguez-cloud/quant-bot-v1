import pandas as pd
import logging

REQUIRED_COLUMNS = ['Open', 'High', 'Low', 'Close', 'Volume']


def validate_dataframe(df, symbol=""):
    if df is None:
        logging.error(f"DataFrame is None {f'for {symbol}' if symbol else ''}")
        return False

    if df.empty:
        logging.error(f"DataFrame is empty {f'for {symbol}' if symbol else ''}")
        return False

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        logging.error(f"Missing columns: {missing}")
        return False

    if not isinstance(df['Close'], pd.Series):
        logging.error("Close column is not a Series")
        return False

    if df['Close'].isna().all():
        logging.error("Close column is all NaN")
        return False

    return True


def validate_signal(result):
    if not isinstance(result, dict):
        return False

    required_keys = ['signal', 'stop_loss', 'take_profit']
    return all(k in result for k in required_keys)