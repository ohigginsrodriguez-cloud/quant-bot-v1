import pandas as pd
import numpy as np
from indicators.atr import calculate_atr
from indicators.bollinger_bands import calculate_bollinger
from indicators.volatility import calculate_volatility

def make_df(n=50):
    close = pd.Series(np.random.uniform(100, 200, n))
    high = close + np.random.uniform(0, 2, n)
    low = close - np.random.uniform(0, 2, n)
    return pd.DataFrame({'Close': close, 'High': high, 'Low': low})

def test_atr_returns_series():
    df = make_df()
    atr = calculate_atr(df)
    assert isinstance(atr, pd.Series), "ATR debe ser pd.Series"
    assert len(atr) == len(df)

def test_atr_no_negative():
    df = make_df()
    atr = calculate_atr(df).dropna()
    assert (atr >= 0).all(), "ATR no puede ser negativo"

def test_bollinger_upper_above_lower():
    df = make_df()
    lower, upper = calculate_bollinger(df['Close'])
    valid = lower.dropna()
    valid_upper = upper.dropna()
    assert (valid_upper.values >= valid.values).all(), "Upper band debe ser >= lower band"

def test_volatility_requires_series():
    try:
        calculate_volatility(1.234, 10)
        assert False, "Debe lanzar ValueError"
    except ValueError:
        pass

if __name__ == "__main__":
    test_atr_returns_series()
    test_atr_no_negative()
    test_bollinger_upper_above_lower()
    test_volatility_requires_series()
    print("All tests passed")