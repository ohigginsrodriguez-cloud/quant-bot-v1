import yfinance as yf
import logging
import pandas as pd

def load_data(symbol, period, interval):
    try:
        df = yf.download(symbol, period=period, interval=interval)

        # Validar datos vacíos
        if df.empty:
            logging.warning(f'No data found for {symbol}')
            return None
        
        # Manejar MultiIndex en columnas (si existe)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)

        # Normalizar volumen
        if 'Volume' in df.columns:
            df['Volume'] = df['Volume'].replace(0, pd.NA)

        return df
    
    except Exception as e:
        logging.error(f'Error downloading data: {e}')
        return None