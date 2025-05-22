import pytz

# Timezone
BD_TZ = pytz.timezone("Asia/Dhaka")  # GMT+6

# Default values
DEFAULT_SYMBOL = "EURUSD"
SSL_WINDOW = 10

# RSI reference levels
RSI_UPPER = 80  # Overbought
RSI_UPPER_Z = 70  # Overbought
RSI_LOWER = 20  # Oversold
RSI_LOWER_Z = 30  # Oversold
RSI_MID = 50    # Midline

# Timeframe mapping
TIMEFRAME_MAP = {
    "1D": "TIMEFRAME_D1",
    "4H": "TIMEFRAME_H4",
    "1H": "TIMEFRAME_H1",
    "15M": "TIMEFRAME_M15",
    "5M": "TIMEFRAME_M5",
    "1M": "TIMEFRAME_M1"
}

# Autoplay speed presets
SPEED_PRESETS = {
    "🐢 Slow (2s)": 2.0,
    "🐇 Fast (0.5s)": 0.5,
    "⚡ Very Fast (0.2s)": 0.2,
    "⏩ Ultra Fast (0.1s)": 0.1,
}
DEFAULT_SPEED_LABEL = "🐇 Fast (0.5s)"