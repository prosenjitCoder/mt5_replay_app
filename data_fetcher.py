import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
from config import BD_TZ
import streamlit as st
from typing import Optional, List

def initialize_mt5():
    """Initialize MT5 connection only if not already connected"""
    if not mt5.initialize():
        if not mt5.initialize():  # Try one more time
            raise ConnectionError("Failed to connect to MetaTrader5. Check terminal status.")
    # Remove the print statement to avoid console spam
    print("MT5 initialized successfully")  # Comment out or remove this line

def get_symbols() -> List[str]:
    """Fetch all symbols available in MT5"""
    symbols = mt5.symbols_get()
    return sorted([s.name for s in symbols])

def fetch_data(
    symbol: str,
    timeframe: int,
    from_date: datetime,
    to_date: datetime,
    max_retries: int = 3
) -> pd.DataFrame:
    """Fetch OHLC data from MT5 with retry logic"""
    for attempt in range(max_retries):
        try:
            rates = mt5.copy_rates_range(symbol, timeframe, from_date, to_date)
            if rates is None:
                raise ValueError(f"No data returned for {symbol} {timeframe}")
                
            df = pd.DataFrame(rates)
            df["time"] = pd.to_datetime(df["time"], unit="s").dt.tz_localize("UTC").dt.tz_convert(BD_TZ)
            return df[["time", "open", "high", "low", "close", "tick_volume"]]
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise ConnectionError(f"Failed after {max_retries} attempts: {str(e)}")
            print(f"Retrying... (Attempt {attempt + 1}/{max_retries})")
            mt5.shutdown()
            initialize_mt5()