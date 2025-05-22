import pandas as pd
from config import SSL_WINDOW

def fetch_ssl_channel(dataframe: pd.DataFrame):
    high, low, close = dataframe["high"], dataframe["low"], dataframe["close"]
    sma_high = high.rolling(window=SSL_WINDOW).mean()
    sma_low = low.rolling(window=SSL_WINDOW).mean()

    hlv = pd.Series(0, index=close.index)
    hlv[close > sma_high] = 1
    hlv[close < sma_low] = -1

    ssl_up = pd.Series(index=close.index, dtype="float64")
    ssl_down = pd.Series(index=close.index, dtype="float64")

    ssl_up[hlv == 1] = sma_high[hlv == 1]
    ssl_down[hlv == 1] = sma_low[hlv == 1]
    ssl_up[hlv == -1] = sma_low[hlv == -1]
    ssl_down[hlv == -1] = sma_high[hlv == -1]

    return ssl_up.ffill(), ssl_down.ffill()

def compute_rsi(series: pd.Series, period: int) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def add_emas(df, ema1_period=None, ema2_period=None):
    if ema1_period:
        df["EMA1"] = df["close"].ewm(span=ema1_period).mean()
    else:
        df["EMA1"] = None
    
    if ema2_period:
        df["EMA2"] = df["close"].ewm(span=ema2_period).mean()
    else:
        df["EMA2"] = None
    
    return df