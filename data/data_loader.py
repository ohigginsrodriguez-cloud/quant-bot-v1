import yfinance as yf
import logging
import pandas as pd

def load_data(symbol, period, interval):
    try:
        df = yf.download(symbol, period=period, interval=interval, auto_adjust=True)

        # Manejar MultiIndex en columnas
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Eliminar columnas duplicadas si las hay
        df = df.loc[:, ~df.columns.duplicated()]

        # Validar datos vacíos
        if df.empty:
            logging.warning(f'No data found for {symbol}')
            return None

        # Asegurar que Close sea Serie y no DataFrame
        if isinstance(df['Close'], pd.DataFrame):
            df['Close'] = df['Close'].squeeze()

        # Normalizar volumen
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].replace(0, pd.NA)

        logging.info(f"Loaded {len(df)} candles for {symbol}")
        return df
    
    except Exception as e:
        logging.error(f'Error downloading data: {e}')
        return None