from datetime import datetime, timedelta
import streamlit as st
from config import *

def create_sidebar():
    st.sidebar.title("Replay Controls")
    
    # Symbol selection
    symbol_names = st.session_state.get('symbol_names', [])
    default_index = symbol_names.index(DEFAULT_SYMBOL) if DEFAULT_SYMBOL in symbol_names else 0
    symbol = st.sidebar.selectbox("Symbol", options=symbol_names, index=default_index)
    
    # Timeframe selection
    tf_labels = list(TIMEFRAME_MAP.keys())
    prev_tf_label = st.session_state.get("prev_tf_label", "1H")
    selected_tf_label = st.sidebar.selectbox("Time-frame", tf_labels, index=tf_labels.index(prev_tf_label))
    
    # Date range
    today = datetime.now().date()
    default_from = today - timedelta(days=7)
    default_to = today
    from_date = st.sidebar.date_input("From", default_from)
    to_date = st.sidebar.date_input("To", default_to)
    
    # Chart settings
    screen_bars = st.sidebar.slider("Candles on screen", 20, 150, 80)
    chart_h = st.sidebar.slider("Chart height (px)", 500, 1200, 880)
    
    # Indicators
    st.sidebar.subheader("Indicators")
    show_ssl = st.sidebar.checkbox("Show SSL Channel", value=True)
    
    show_ema1 = st.sidebar.checkbox("Show EMA 1", value=True)
    ema1_period = st.sidebar.number_input("EMA 1 Period", min_value=1, max_value=500, value=21, step=1) if show_ema1 else None
    
    show_ema2 = st.sidebar.checkbox("Show EMA 2", value=False)
    ema2_period = st.sidebar.number_input("EMA 2 Period", min_value=1, max_value=500, value=50, step=1) if show_ema2 else None
    
    show_rsi = st.sidebar.checkbox("Show RSI", value=False)
    rsi_period = st.sidebar.number_input("RSI Period", min_value=2, max_value=100, value=14, step=1) if show_rsi else None
    
    show_sessions = st.sidebar.checkbox("Show Sessions (London/NY)", value=False)
    
    # Autoplay
    autoplay = st.sidebar.checkbox("Autoplay")
    selected_speed_label = st.sidebar.selectbox(
        "Autoplay Speed",
        options=list(SPEED_PRESETS.keys()),
        index=list(SPEED_PRESETS.keys()).index(DEFAULT_SPEED_LABEL)
    )
    
    return {
        'symbol': symbol,
        'selected_tf_label': selected_tf_label,
        'from_date': from_date,
        'to_date': to_date,
        'screen_bars': screen_bars,
        'chart_h': chart_h,
        'show_ssl': show_ssl,
        'show_ema1': show_ema1,
        'ema1_period': ema1_period,
        'show_ema2': show_ema2,
        'ema2_period': ema2_period,
        'show_rsi': show_rsi,
        'rsi_period': rsi_period,
        'show_sessions': show_sessions,
        'autoplay': autoplay,
        'selected_speed_label': selected_speed_label
    }